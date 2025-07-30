import collections
import logging

import torch
from lightning import LightningDataModule
from torch.utils.data import DataLoader

from gammalearn.data.concat_dataset_utils import split_dataset


class BaseDataModule(LightningDataModule):
    """
    Create datasets and dataloaders.
    Parameters
    ----------
    experiment (Experiment): the experiment
    """

    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment
        self.logger = logging.getLogger(__name__)
        self.train_set = None
        self.val_set = None
        self.test_sets = None  # List
        self.collate_fn = torch.utils.data.default_collate

    def setup(self, stage=None):
        """
        In the case that the train and the test data modules are different, two setup functions are defined in order to
         prevent from loading data twice.
        """
        self.setup_train()
        self.setup_test()

    def setup_train(self):
        """
        This function is used if train is set to True in experiment setting file
        """
        self.logger.info("Start creating datasets")
        self.logger.info("look for data files")

        # Creation of the global train/val dataset
        datasets = self.get_dataset(train=True)
        assert datasets, "Dataset is empty !"

        # Creation of subsets train and validation
        train_datasets, val_datasets = split_dataset(datasets, self.experiment.validating_ratio)

        self.train_set = train_datasets
        self.logger.info("training set length : {}".format(len(self.train_set)))

        self.val_set = val_datasets
        try:
            assert len(self.val_set) > 0
        except AssertionError as e:
            self.logger.exception("Validating set must contain data")
            raise e
        self.logger.info("validating set length : {}".format(len(self.val_set)))

    def setup_test(self):
        """
        This function is used if test is set to True in experiment setting file.
        If no data module test is provided, test is completed on the validation set.
        If neither a data module test nor a validation set is provided, an error will be raised.
        """
        if self.experiment.data_module_test is not None:
            # Look for specific data parameters
            if self.experiment.test_dataset_parameters is not None:
                self.experiment.dataset_parameters.update(self.experiment.test_dataset_parameters)

            # Creation of the test datasets
            self.test_sets = self.get_dataset(train=False)
        else:  # Test is set to False in experiment setting file
            assert self.val_set is not None, "Test is required but no test file is provided and val_set is None"
            self.test_sets = [self.val_set]
        self.logger.info("test set length : {}".format(torch.tensor([len(t) for t in self.test_sets]).sum()))

    def train_dataloader(self):
        r"""Return the training dataloader"""

        training_loader = DataLoader(
            self.train_set,
            batch_size=self.experiment.batch_size,
            shuffle=True,
            drop_last=True,
            num_workers=self.experiment.dataloader_workers,
            pin_memory=self.experiment.pin_memory,
            collate_fn=self.collate_fn,
        )
        self.logger.info("training loader length : {} batches".format(len(training_loader)))
        return training_loader

    def val_dataloader(self):
        r"""Return the validation dataloader"""
        validating_loader = DataLoader(
            self.val_set,
            batch_size=self.experiment.batch_size,
            shuffle=False,
            num_workers=self.experiment.dataloader_workers,
            drop_last=True,
            pin_memory=self.experiment.pin_memory,
            collate_fn=self.collate_fn,
        )
        self.logger.info("validating loader length : {} batches".format(len(validating_loader)))
        return validating_loader

    def test_dataloaders(self):
        r"""Return the test dataloaders"""
        test_loaders = [
            DataLoader(
                test_set,
                batch_size=self.experiment.test_batch_size,
                shuffle=False,
                drop_last=False,
                num_workers=self.experiment.dataloader_workers,
            )
            for test_set in self.test_sets
        ]
        self.logger.info("test loader length : {} data loader(s)".format(len(test_loaders)))
        self.logger.info("test loader length : {} batches".format(torch.tensor([len(t) for t in test_loaders]).sum()))
        return test_loaders

    def get_dataset(self, train):
        """
        DataModule-specific method to be overwritten to load the dataset.
        """
        return NotImplementedError

    def get_collate_fn(self):
        """
        This function prevent bug from mixing MC and real data.
        """
        numpy_type_map = {
            "float64": torch.DoubleTensor,
            "float32": torch.FloatTensor,
            "float16": torch.HalfTensor,
            "int64": torch.LongTensor,
            "int32": torch.IntTensor,
            "int16": torch.ShortTensor,
            "int8": torch.CharTensor,
            "uint8": torch.ByteTensor,
            "bool": torch.BoolTensor,
        }

        def collate_fn(batch: list):
            """
            The batch is a mixture of nested dictionary, list, number and numpy arrays. This function
            stacks each leaf element into an array, and transforms to torch.tensor or torch dtypes.
            Puts each data field into a tensor with outer dimension batch size. From:
            https://github.com/hughperkins/pytorch-pytorch/blob/c902f1cf980eef27541f3660c685f7b59490e744/torch/utils/data/dataloader.py#L91
            """
            error_msg = "batch must contain tensors, numbers, dicts or lists; found {}"
            elem_type = type(batch[0])
            if torch.is_tensor(batch[0]):
                out = None
                return torch.stack(batch, 0, out=out)
            elif elem_type.__module__ == "numpy" and elem_type.__name__ != "str_" and elem_type.__name__ != "string_":
                elem = batch[0]
                if elem_type.__name__ == "ndarray":
                    return torch.stack([torch.from_numpy(b) for b in batch], 0)
                if elem.shape == ():  # scalars
                    py_type = float if elem.dtype.name.startswith("float") else int
                    return numpy_type_map[elem.dtype.name](list(map(py_type, batch)))
            elif isinstance(batch[0], int):
                return torch.LongTensor(batch)
            elif isinstance(batch[0], float):
                return torch.DoubleTensor(batch)
            elif isinstance(batch[0], (str, bytes)):
                return batch
            elif isinstance(batch[0], collections.abc.Mapping):
                # If MC and real data in target, find the common keys
                common_keys = set(batch[0].keys())
                for d in batch[1:]:
                    common_keys.intersection_update(d.keys())
                return {key: collate_fn([d[key] for d in batch]) for key in common_keys}
            elif isinstance(batch[0], collections.Sequence):
                transposed = zip(*batch)
                return [collate_fn(samples) for samples in transposed]

            raise TypeError((error_msg.format(type(batch[0]))))

        return collate_fn


def fetch_data_module_settings(experiment, train, domain):
    """
    Load the data module described in the experiment setting file.

    Allows to parse the data module part of the settings, when domain adaptation is used.

    Parameters
    ----------
    experiment: the experiment instance
    train: True or False depending on the train/test context
    domain: 'source' or 'target' if domain adaptation or None if no domain adaptation

    Returns
    -------
    The data module.
    """
    if domain is None:  # No domain adaptation
        return experiment.data_module_train if train else experiment.data_module_test
    else:  # Domain adaptation
        return experiment.data_module_train[domain] if train else experiment.data_module_test
