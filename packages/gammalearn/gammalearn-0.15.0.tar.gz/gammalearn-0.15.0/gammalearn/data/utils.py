import logging
import os
import random

import numpy as np
import tables


def browse_folder(data_folder, extension=None):
    """
    Browse folder given to find hdf5 files
    Parameters
    ----------
    data_folder (string)
    extension (string)

    Returns
    -------
    set of hdf5 files
    """
    logger = logging.getLogger(__name__)
    if extension is None:
        extension = [".hdf5", ".h5"]
    try:
        assert isinstance(extension, list)
    except AssertionError as e:
        logger.exception("extension must be provided as a list")
        raise e
    logger.debug("browse folder")
    file_set = set()
    for dirname, dirnames, filenames in os.walk(data_folder):
        logger.debug("found folders : {}".format(dirnames))
        logger.debug("in {}".format(dirname))
        logger.debug("found files : {}".format(filenames))
        for file in filenames:
            filename, ext = os.path.splitext(file)
            if ext in extension:
                file_set.add(dirname + "/" + file)
    return file_set


def find_datafiles(data_folders, files_max_number=-1):
    """
    Find datafiles in the folders specified
    Parameters
    ----------
    data_folders (list): the folders where the data are stored
    files_max_number (int, optional): the maximum number of files to keep per folder

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    logger.debug("data folders: {}".format(data_folders))

    # We can have several folders
    datafiles = set()

    # If the path specified in the experiment settings is not a list, turns it into a list of one element
    data_folders = [data_folders] if isinstance(data_folders, str) else data_folders

    # If files_max_number is an integer, turns it into a list of one element.
    files_max_number = [files_max_number] if isinstance(files_max_number, int) else files_max_number

    # If files_max_number is a list of multiple integers, each integer specifies the number of data to load for the
    # corresponding folder, otherwise, give the same max_number for all folders
    assert len(files_max_number) == 1 or len(files_max_number) == len(
        data_folders
    ), "Number of max files not matching number of folders."
    if not (len(files_max_number) == len(data_folders)):
        files_max_number *= len(data_folders)

    for folder, max_number in zip(data_folders, files_max_number):
        logger.debug("data folder : {}".format(folder))
        dataf = list(browse_folder(folder))
        random.shuffle(
            dataf
        )  # shuffle the list so that we don't use consecutive files of real LST data, but a uniform sampling on all the files
        # max_number of value -1 means load all data
        if max_number and 0 < max_number <= len(dataf):
            dataf = dataf[0:max_number]
        dataf = set(dataf)
        datafiles.update(dataf)

    return datafiles


def is_datafile_healthy(file_path):
    """
    Check that the data file does not contain empty dataset

    Parameters
    ----------
    file_path (str): the path to the file

    Returns
    -------
    A boolean
    """
    dataset_emptiness = []

    _, ext = os.path.splitext(file_path)
    if ext in [".hdf5", ".h5"]:
        with tables.File(file_path, "r") as f:
            for n in f.walk_nodes():
                if isinstance(n, tables.Table):
                    dataset_emptiness.append(n.shape[0])
    return not np.any(np.array(dataset_emptiness) == 0)
