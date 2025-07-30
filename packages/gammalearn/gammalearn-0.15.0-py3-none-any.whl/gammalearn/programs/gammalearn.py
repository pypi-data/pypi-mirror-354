import argparse
import logging
import os
import shutil
from importlib.metadata import version as runtime_version
import lightning
import torch
import torch.backends.cudnn as cudnn
from lightning.pytorch.callbacks import DeviceStatsMonitor, LearningRateMonitor, ModelCheckpoint

from gammalearn.configuration.gl_logging import LOGGING_CONFIG
from gammalearn.configuration.save_configuration import dump_experiment_config
from gammalearn.data.telescope_geometry import WrongGeometryError, get_dataset_geom, inject_geometry_into_parameters
from gammalearn.experiment_paths import prepare_experiment_folder
from gammalearn.gammalearn_lightning_module import LitGLearnModule
from gammalearn.experiment_runner import load_experiment

def build_argparser():
    """Construct main argument parser for the ``gammalearn`` script

    Returns
    -------
    argparse.ArgumentParser
        Argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Run a GammaLearn experiment from a configuration file. An experiment can be a training, a testing or both. See examples configuration files in the examples folder."
    )
    parser.add_argument("configuration_file", help="path to configuration file")
    # TODO: fast_debug activates the fast_dev_run of the lithgning Trainer which allows to do only a few batches of train, val and test
    # in practice, we don't use it
    parser.add_argument("--fast_debug", help="log useful information for debug purpose", action="store_true")
    parser.add_argument("--logfile", help="whether to write the log on disk", action="store_true")
    parser.add_argument("--version", action="version", version=runtime_version("gammalearn"))

    return parser


def main():
    # For better performance (if the input size does not vary from a batch to another)
    cudnn.benchmark = True

    # At the beginning of the main process, local_rank is set to None.
    # When multiple processes are running in parallel (e.g. while loading some data), each process will be assigned to a
    # positive valued local_rank. When each sub-process is started, it will run the main() function. Setting this
    # variable at the beginning ensure that some actions will only occur once and not within the other sub-process.
    local_rank = os.getenv("LOCAL_RANK")

    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("gammalearn")

    # Parse script arguments
    logger.info("parse arguments")

    parser = build_argparser()
    args = parser.parse_args()
    configuration_file = args.configuration_file
    fast_debug = args.fast_debug
    logfile = args.logfile

    # Update logging config
    LOGGING_CONFIG["handlers"]["console"]["formatter"] = "console_debug" if fast_debug else "console_info"
    LOGGING_CONFIG["loggers"]["gammalearn"]["level"] = "DEBUG" if fast_debug else "INFO"
    logging.config.dictConfig(LOGGING_CONFIG)

    logger = logging.getLogger("gammalearn")

    # load settings file
    if local_rank is None:
        logger.info(f"load settings from {configuration_file}")

    experiment = load_experiment(configuration_file)

    # prepare folders
    if local_rank is None:
        logger.info("prepare folders")
        prepare_experiment_folder(experiment.main_directory, experiment.experiment_name)

    # TODO: since we always train in slurm, output is logged already. Remove ?
    if logfile:
        LOGGING_CONFIG["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "filename": "{}/{}/{}.log".format(
                experiment.main_directory, experiment.experiment_name, experiment.experiment_name
            ),
            "mode": "w",
            "formatter": "detailed_debug" if fast_debug else "detailed_info",
        }
        LOGGING_CONFIG["loggers"]["gammalearn"]["handlers"].append("file")
        logging.config.dictConfig(LOGGING_CONFIG)

    if local_rank is None:
        logger.info("gammalearn {}".format(runtime_version("gammalearn")))
        # save config(settings)
        logger.info("save configuration file")
        shutil.copyfile(
            configuration_file,
            "{}/{}/{}_settings.py".format(
                experiment.main_directory, experiment.experiment_name, experiment.experiment_name
            ),
        )
        # dump settings
        dump_experiment_config(experiment)

    # set seed
    if experiment.random_seed is not None:
        lightning.pytorch.seed_everything(experiment.random_seed)

    # Check that the geometries are all the same
    # TODO: won't work when doing stereo
    geometries = []
    # Load train data module
    if experiment.train is True:
        gl_data_module_train = experiment.data_module_train["module"](experiment)
        gl_data_module_train.setup_train()
        train_dataloaders = gl_data_module_train.train_dataloader()
        val_dataloaders = gl_data_module_train.val_dataloader()
        get_dataset_geom(gl_data_module_train.train_set, geometries)
    else:
        train_dataloaders = None
        val_dataloaders = None
    # Load test data module
    if experiment.test is True:
        if experiment.data_module_test is not None:
            gl_data_module_test = experiment.data_module_test["module"](experiment)
            gl_data_module_test.setup_test()
            test_dataloaders = gl_data_module_test.test_dataloaders()
            get_dataset_geom(gl_data_module_test.test_sets, geometries)
        else:  # If no test data module, use validation data from train data module
            try:
                assert val_dataloaders is not None
            except AssertionError as err:
                logger.exception("No test data module is provided and validation data loader is None.")
                raise err
            test_dataloaders = [val_dataloaders]
    else:
        test_dataloaders = None

    # testing if all geometries are equal
    if len(set(geometries)) != 1:
        raise WrongGeometryError("There are different geometries in the train and the test datasets")

    # Add the geometry to the fields to load in the batch, so that the transformers can compute the positional encoding based on geometry
    experiment.net_parameters_dic = inject_geometry_into_parameters(experiment.net_parameters_dic, geometries[0])

    # TODO: is it usefull to support something else than "fork" (we never run on windows)
    # Define multiprocessing start method
    try:
        assert torch.multiprocessing.get_start_method() == experiment.mp_start_method
    except AssertionError:
        torch.multiprocessing.set_start_method(experiment.mp_start_method, force=True)
    if local_rank is None:
        logger.info("mp start method: {}".format(torch.multiprocessing.get_start_method()))

    # Reset seed:
    # because random is used in trainers.setup_train and trainer.setup_test
    # but we want the seed to always be the same before we initialize the model for comparison of models between experiments (that can have different data)
    if experiment.random_seed is not None:
        lightning.pytorch.seed_everything(experiment.random_seed)

    if local_rank is None:
        logger.info("Save net definition file")
        if experiment.net_definition_file is not None:
            shutil.copyfile(
                experiment.net_definition_file,
                "{}/{}/nets.py".format(experiment.main_directory, experiment.experiment_name),
            )

    # load lightning module (which inits the model)
    gl_lightning_module = LitGLearnModule(experiment)
    checkpoint_callback = ModelCheckpoint(**experiment.checkpointing_options)

    # Log learning rates
    callbacks = [
        checkpoint_callback,
        LearningRateMonitor(logging_interval="epoch"),
    ]

    if experiment.monitor_device and experiment.gpus not in [None, 0]:
        callbacks.append(DeviceStatsMonitor())

    callbacks.extend(experiment.training_callbacks)
    callbacks.extend(experiment.test_callbacks)
    unique_callbacks = {callback.__class__: callback for callback in callbacks}
    callbacks = list(unique_callbacks.values())

    # prepare logger
    if experiment.train:
        experiment.trainer_logger.setup(experiment, gl_lightning_module)
        if local_rank is None:
            logger.info(
                "{} run directory: {} ".format(
                    experiment.trainer_logger.type, experiment.trainer_logger.get_run_directory(experiment)
                )
        )

    # Prepare profiler
    if experiment.profiler is not None:
        profiler = experiment.profiler["profiler"](
            dirpath=os.path.join(experiment.main_directory, experiment.experiment_name),
            filename=os.path.join(experiment.experiment_name + ".prof"),
            **experiment.profiler["options"],
        )
    else:
        profiler = None

    # Run !
    if fast_debug:
        trainer = lightning.Trainer(fast_dev_run=True, gpus=-1, profiler=profiler)
        trainer.fit(gl_lightning_module, train_dataloaders=train_dataloaders, val_dataloaders=val_dataloaders)
        # TODO remove when lightning bug is fixed
        if experiment.profiler is not None:
            profiler = experiment.profiler["profiler"](
                dirpath=os.path.join(experiment.main_directory, experiment.experiment_name),
                filename=os.path.join(experiment.experiment_name + ".prof"),
                **experiment.profiler["options"],
            )
            trainer.profiler = profiler

        trainer.test(gl_lightning_module, dataloaders=test_dataloaders)
    else:
        if experiment.train:
            trainer = lightning.Trainer(
                default_root_dir=os.path.join(experiment.main_directory, experiment.experiment_name),
                accelerator=experiment.accelerator,
                devices=experiment.gpus if experiment.gpus is not None else "auto",
                strategy=experiment.strategy,
                max_epochs=experiment.max_epochs,
                logger=experiment.trainer_logger.logger,
                log_every_n_steps=experiment.log_every_n_steps,
                check_val_every_n_epoch=experiment.check_val_every_n_epoch,
                callbacks=callbacks,
                profiler=profiler,
            )
            logger.info("Rank {}: Train model".format(gl_lightning_module.local_rank))
            trainer.fit(
                gl_lightning_module,
                train_dataloaders=train_dataloaders,
                val_dataloaders=val_dataloaders,
                ckpt_path=experiment.checkpoint_path,
            )
            if experiment.test:
                trainer = lightning.Trainer(
                    default_root_dir=os.path.join(experiment.main_directory, experiment.experiment_name),
                    accelerator=experiment.accelerator,
                    devices=1,  # Force 1 GPU for test
                    strategy=experiment.strategy,
                    callbacks=callbacks,
                    profiler=profiler,
                )
                logger.info("Rank {}: Test model".format(gl_lightning_module.local_rank))
                trainer.test(gl_lightning_module, dataloaders=test_dataloaders)
                gl_lightning_module.reset_test_data()
        elif experiment.test:
            trainer = lightning.Trainer(
                default_root_dir=os.path.join(experiment.main_directory, experiment.experiment_name),
                accelerator=experiment.accelerator,
                devices=1,  # Force 1 GPU for test
                # Recommended with ddp strategy see https://gitlab.in2p3.fr/gammalearn/gammalearn/-/issues/101
                strategy=experiment.strategy,
                callbacks=callbacks,
            )
            logger.info("Rank {}: Test model".format(gl_lightning_module.local_rank))
            # TODO: check this at config validation time
            assert experiment.checkpoint_path is not None, "To test a model w/o training, there must be a checkpoint"
            map_location = torch.device("cpu") if experiment.gpus == 0 else None
            ckpt = torch.load(experiment.checkpoint_path, map_location=map_location)
            gl_lightning_module.load_state_dict(ckpt["state_dict"], strict=False)
            trainer.test(gl_lightning_module, dataloaders=test_dataloaders)
            # TODO: can remove this reset ?
            gl_lightning_module.reset_test_data()


if __name__ == "__main__":
    main()
