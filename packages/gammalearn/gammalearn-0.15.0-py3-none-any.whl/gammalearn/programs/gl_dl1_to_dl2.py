#!/usr/bin/env python

from __future__ import division, print_function

import argparse
import faulthandler
import logging
import os
from importlib.metadata import version as runtime_version
from logging import Logger
from pathlib import Path
from typing import List

import torch
import torch.backends.cudnn as cudnn
from torch.multiprocessing import Process, Queue
from torch.utils.data import DataLoader
from tqdm import tqdm

from gammalearn.configuration.gl_logging import LOGGING_CONFIG
from gammalearn.data.concat_dataset_utils import create_dataset
from gammalearn.data.LST_dataset import BaseLSTDataset
from gammalearn.data.save_results.write_dl2_files import (
    create_dl2_params,
    write_dl2_file,
)
from gammalearn.data.telescope_geometry import WrongGeometryError, get_dataset_geom, inject_geometry_into_parameters
from gammalearn.data.utils import find_datafiles
from gammalearn.experiment_runner import Experiment
from gammalearn.gammalearn_lightning_module import LitGLearnModule
from gammalearn.experiment_runner import load_experiment

faulthandler.enable()


def build_argparser():
    r"""Construct main argument parser for the ``gl_dl1_to_dl2`` script

    Returns
    -------
    argparse.ArgumentParser
        The argument parser of this entrypoint
    """
    parser = argparse.ArgumentParser(description="Convert DL1 files to DL2 files using a trained model.")
    parser.add_argument("settings", type=Path, help="Path to the experiment settings file")
    parser.add_argument("checkpoint", type=Path, help="Path to the checkpoint file to load")
    parser.add_argument("dl1", type=Path, help="Directory path to the dl1 files")
    parser.add_argument("dl2", type=Path, help="Directory path to write the dl2 files")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-queue", type=int, default=20)
    parser.add_argument("--preprocess-workers", type=int, default=4)
    parser.add_argument("--dataloader-workers", type=int, default=4)
    parser.add_argument("--version", action="version", version=runtime_version("gammalearn"))
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")

    return parser


def dl2_filename(dl1_filename: Path) -> Path:
    return os.path.basename(dl1_filename).replace("dl1", "dl2")


def inject_geometry(dataset: BaseLSTDataset, experiment: Experiment) -> Experiment:
    geometries = []
    get_dataset_geom(dataset, geometries)
    if len(set(geometries)) != 1:  # Testing if all geometries are equal
        raise WrongGeometryError("There are different geometries in the train and the test datasets")
    experiment.net_parameters_dic = inject_geometry_into_parameters(experiment.net_parameters_dic, geometries[0])
    return experiment


def load_module_from_checkpoint(
    experiment: Experiment, dataset: BaseLSTDataset, checkpoint_path: Path
) -> LitGLearnModule:
    experiment = inject_geometry(dataset, experiment)
    module = LitGLearnModule.load_from_checkpoint(checkpoint_path, experiment=experiment, strict=False)
    return module


def get_model(module: LitGLearnModule, device: str) -> torch.nn.Module:
    model = module.net
    model.eval()
    model.to(device)
    return model


def update_logging_config(logs_dir: Path) -> Logger:
    LOGGING_CONFIG["loggers"]["gammalearn"]["level"] = "INFO"
    LOGGING_CONFIG["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": logs_dir.joinpath("dl1_to_dl2.log"),
        "mode": "a",
        "formatter": "detailed_info",
    }
    LOGGING_CONFIG["loggers"]["gammalearn"]["handlers"].append("file")
    logger = logging.getLogger("gammalearn")
    logging.config.dictConfig(LOGGING_CONFIG)
    return logger


def get_output_path(dl2_path: Path, hdf5_file_path: str, overwrite: bool) -> Path:
    output_path = dl2_path.joinpath(dl2_filename(hdf5_file_path))
    if os.path.exists(output_path) and overwrite:
        os.remove(output_path)
    return output_path


def terminate(processes: List[Process]) -> None:
    for p in processes:
        p.terminate()


def main():
    # For better performance (if the input size does not vary from a batch to another)
    cudnn.benchmark = True

    parser = build_argparser()
    args = parser.parse_args()

    # Create DL2 directory and logs directory
    dl2_path = args.dl2
    logs_dir = dl2_path.joinpath("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = update_logging_config(logs_dir)

    # Get dl1 files
    dl1_file_list = find_datafiles([args.dl1])
    dl2_outputs = [dl2_path.joinpath(dl2_filename(dl1_file)) for dl1_file in dl1_file_list]
    if not args.overwrite and any([dl2_file.exists() for dl2_file in dl2_outputs]):
        raise FileExistsError(
            f"Output files already exists in {dl2_path}. Use --overwrite to overwrite existing files."
        )

    # Load experiment settings
    logger.info(f"Load settings from {args.settings}")
    experiment = load_experiment(args.settings)
    # Transforms should exist and be loaded from the test module, if any
    experiment.dataset_parameters["transform"] = experiment.data_module_test.get("transform", None)
    module = None
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load file names
    logger.info("Find dl1 files and populate file queue")
    file_queue = Queue()
    for file in tqdm(dl1_file_list, desc="Queueing files"):
        file_queue.put(file)

    # Create a group of parallel writers and start them
    dl1_queue = Queue(args.max_queue)
    processes = []
    for rank in range(args.preprocess_workers):
        p = Process(
            target=create_dataset,
            args=(file_queue, dl1_queue, experiment.dataset_class, experiment.dataset_parameters),
        )
        p.start()
        processes.append(p)

    # Run the main loop
    logger.info("Start processing dl1 datasets")
    for _ in tqdm(dl1_file_list, desc="Processing dl1 files"):
        try:
            dataset = dl1_queue.get()
            dataloader = DataLoader(dataset, batch_size=args.batch_size, num_workers=args.dataloader_workers)

            if module is None:
                logger.info("Load model")
                module = load_module_from_checkpoint(experiment, dataset, args.checkpoint)
                model = get_model(module, device)

            test_data = {"output": [], "dl1_params": []}
            forward_params = {}

            for batch in tqdm(dataloader, desc="Processing batches", total=len(dataloader)):
                with torch.no_grad():
                    images = batch["image"].to(device)
                    forward_params["transform_params"] = batch.get("transform_params", {})
                    output = model(images, **forward_params)

                for k, v in output.items():
                    output[k] = v.cpu()

                test_data["output"].append(output)
                test_data["dl1_params"].append(batch["dl1_params"])

            dl2_params = create_dl2_params(test_data, experiment.dataset_parameters)
            output_path = get_output_path(dl2_path, dataset.hdf5_file_path, args.overwrite)
            write_dl2_file(dl2_params, dataset, output_path)
        except Exception as e:
            logger.error(f"Error processing {dataset.hdf5_file_path}")
            terminate(processes)
            raise e

    logger.info("All files processed")
    terminate(processes)


if __name__ == "__main__":
    main()
