from typing_extensions import deprecated

from gammalearn.data import base_data_module as utils
from gammalearn.data.base_data_module import BaseDataModule
from gammalearn.data.concat_dataset_utils import balance_datasets, shuffle_datasets
from gammalearn.data.domain_adaptation import DomainAdaptationDataset


@deprecated("Digit's Datasets and DataModules are deprecated and will be removed in a future release!")
class VisionDataModule(BaseDataModule):
    """
    Equivalent of the GLearnDataModule but for the digits datasets.

    Parameters
    ----------
    experiment (Experiment): the experiment

    Returns
    -------
    """

    def __init__(self, experiment):
        super().__init__(experiment)

    def get_dataset(self, train):
        max_files = self.experiment.train_files_max_number if train else self.experiment.test_files_max_number
        data_module = utils.fetch_data_module_settings(self.experiment, train=train, domain=None)
        dataset = self.get_dataset_from_path(data_module, train=train, domain="source", max_files=max_files)

        return dataset

    def get_dataset_from_path(self, data_module, train, domain=None, max_files=None):
        datasets = self.experiment.dataset_class(
            paths=data_module["paths"],
            dataset_parameters=self.experiment.dataset_parameters,
            transform=data_module["transform"],
            target_transform=data_module["target_transform"],
            train=train,
            domain=domain,
            max_files=max_files,
            num_workers=self.experiment.preprocessing_workers,
        )

        return [datasets] if not train else datasets


@deprecated("Digit's Datasets and DataModules are deprecated and will be removed in a future release!")
class VisionDomainAdaptationDataModule(VisionDataModule):
    """
    Equivalent of the VisionDataModule but with 2 domains: source and target datasets, for domain adaptation.

    Parameters
    ----------
    experiment (Experiment): the experiment

    Returns
    -------
    """

    def __init__(self, experiment):
        super().__init__(experiment)
        self.dataset_balancing = experiment.dataset_parameters.get("dataset_balancing", False)

    def get_dataset(self, train):
        max_files = self.experiment.train_files_max_number if train else self.experiment.test_files_max_number

        data_module_source = utils.fetch_data_module_settings(self.experiment, train=train, domain="source")
        data_module_target = utils.fetch_data_module_settings(self.experiment, train=train, domain="target")

        dataset_src = self.get_dataset_from_path(data_module_source, train=train, domain="source", max_files=max_files)
        dataset_trg = self.get_dataset_from_path(data_module_target, train=train, domain="target", max_files=max_files)

        if self.dataset_balancing:
            dataset_src, dataset_trg = balance_datasets(dataset_src, dataset_trg)
        else:
            dataset_src, dataset_trg = shuffle_datasets(dataset_src, dataset_trg)

        return DomainAdaptationDataset(dataset_src, dataset_trg)
