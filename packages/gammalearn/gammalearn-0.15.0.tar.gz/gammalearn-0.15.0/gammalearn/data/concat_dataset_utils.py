import logging
from functools import partial

import torch
import torch.multiprocessing as mp
import tqdm
from torch.multiprocessing import Queue
from torch.utils.data import Dataset, Subset

from gammalearn.configuration.gl_logging import LOGGING_CONFIG
from gammalearn.data import utils as utils
from gammalearn.data.LST_dataset import BaseLSTDataset


def create_dataset_worker(file, dataset_class, train, **kwargs):
    """Instantiate a dataset and apply filters on events. If no events are left in the dataset: returns None."""
    torch.set_num_threads(1)
    # Reload logging config (lost by spawn)
    logging.config.dictConfig(LOGGING_CONFIG)

    if utils.is_datafile_healthy(file):
        dataset = dataset_class(file, train=train, **kwargs)
        if kwargs.get("image_filter") is not None:
            dataset.filter_image(kwargs.get("image_filter"))
        if kwargs.get("event_filter") is not None:
            dataset.filter_event(kwargs.get("event_filter"))
        if len(dataset) > 0:
            return dataset


def create_datasets(datafiles_list, experiment, train=True, **kwargs):
    """
    Create all datasets from datafiles list, using a pool of processes to create the datasets in parallel
    TODO: is this slow due to copy at the end of threads to move data to main thread ?

    Parameters
    ----------
    datafiles (List) : files to load data from
    experiment (Experiment): the experiment

    Returns
    -------
    Datasets
    """

    logger = logging.getLogger("gammalearn")
    assert datafiles_list, "The data file list is empty !"

    logger.info("length of data file list : {}".format(len(datafiles_list)))
    # We get spawn context because fork can cause deadlock in sub-processes
    # in multi-threaded programs (especially with logging)
    ctx = mp.get_context("spawn")
    if experiment.preprocessing_workers > 0:
        num_workers = experiment.preprocessing_workers
    else:
        num_workers = 1
    pool = ctx.Pool(processes=num_workers)
    datasets = list(
        tqdm.tqdm(
            pool.imap(
                partial(create_dataset_worker, dataset_class=experiment.dataset_class, train=train, **kwargs),
                datafiles_list,
            ),
            total=len(datafiles_list),
            desc="Load data files",
        )
    )

    return datasets


def split_dataset(datasets, ratio):
    """Split a list of datasets into a train and a validation set. Datasets are shuffled before the split
    between train and test.

    Parameters
    ----------
    datasets (list of Dataset): the list of datasets
    ratio (float): the ratio of data for validation

    Returns
    -------
    train set, validation set

    """
    # Creation of subset train and test
    assert 1 > ratio > 0, "Validating ratio must be greater than 0 and smaller than 1."

    train_max_index = int(len(datasets) * (1 - ratio))
    shuffled_indices = torch.randperm(len(datasets)).numpy()
    assert isinstance(datasets, Dataset)
    train_datasets = Subset(datasets, shuffled_indices[:train_max_index])
    val_datasets = Subset(datasets, shuffled_indices[train_max_index:])

    return train_datasets, val_datasets


def shuffle_dataset(dataset: Dataset, max_index: int = -1) -> Dataset:
    shuffled_indices = torch.randperm(len(dataset)).numpy()
    return Subset(dataset, shuffled_indices[:max_index])


def shuffle_datasets(source_dataset: Dataset, target_dataset: Dataset, max_index: int = -1) -> tuple:
    source_dataset = shuffle_dataset(source_dataset, max_index)
    target_dataset = shuffle_dataset(target_dataset, max_index)

    return source_dataset, target_dataset


def balance_datasets(source_dataset: Dataset, target_dataset: Dataset) -> tuple:
    """If source and targets are different, set the max_index of the shuffling to the
    size of the smaller dataset to have the same number of events of each domain"""
    max_index = min(len(source_dataset), len(target_dataset))
    return shuffle_datasets(source_dataset, target_dataset, max_index)


def create_dataset(
    file_queue: Queue, dl1_queue: Queue, dataset_class: BaseLSTDataset, dataset_parameters: dict
) -> None:
    """
    Create the datasets and fill the correspond queue.

    Parameters
    ----------
    file_queue: (Queue) The queue containing the file names of the dl1 folder.
    dl1_queue: (Queue) The queue containing the datasets.
    dataset_class: (gammalearn.datasets.BaseLSTDataset) the dataset class as specified in the experiment settings file.
    dataset_parameters: (dict) The dataset parameters as specified in the experiment settings file.
    """
    while True:
        if not file_queue.empty():
            file = file_queue.get()
            dataset = create_dataset_worker(file, dataset_class, train=False, **dataset_parameters)
            dl1_queue.put(dataset)
