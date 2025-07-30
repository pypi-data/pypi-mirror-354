import logging

import torch
from torch.utils.data import ConcatDataset, Subset

import gammalearn.data.utils
from gammalearn.configuration.constants import REAL_DATA_ID
from gammalearn.data import base_data_module as utils
from gammalearn.data.base_data_module import BaseDataModule
from gammalearn.data.concat_dataset_utils import balance_datasets, create_datasets, shuffle_datasets
from gammalearn.data.domain_adaptation import GlearnDomainAdaptationDataset


class GLearnDataModule(BaseDataModule):
    def __init__(self, experiment):
        super().__init__(experiment)

    def get_dataset(self, train):
        max_files = self.experiment.train_files_max_number if train else self.experiment.test_files_max_number
        max_events = self.experiment.dataset_size if train else None
        data_module = utils.fetch_data_module_settings(self.experiment, train=train, domain=None)
        dataset = self.get_glearn_dataset_from_path(
            data_module, train, domain=None, max_files=max_files, max_events=max_events
        )

        return dataset

    def get_glearn_dataset_from_path(self, data_module, train, domain=None, max_files=None, max_events=None):
        max_files = -1 if max_files is None else max_files
        if isinstance(max_files, dict) and domain is not None:
            max_files = max_files[domain]
        max_events = {} if max_events is None else max_events
        max_events["default"] = -1

        file_list = gammalearn.data.utils.find_datafiles(data_module["paths"], max_files)
        file_list = list(file_list)
        file_list.sort()

        datasets = create_datasets(
            file_list,
            self.experiment,
            train=train,
            **{"domain": domain},
            **data_module,
            **self.experiment.dataset_parameters,
        )

        if train:
            # Check the dataset list heterogeneity (e.g. simu and real data in target)
            if not (all([dset.simu for dset in datasets]) or not any([dset.simu for dset in datasets])):
                self.collate_fn = self.get_collate_fn()

            # in simulation: files contain either gamma or protons
            # so we need to split them to have a list of only gamma datasets, and only proton datasets.
            dataset_type_dict = {}
            for dset in datasets:
                if dset.simu:
                    particle_type = dset.dl1_params["mc_type"][0]

                    if particle_type in dataset_type_dict:
                        dataset_type_dict[particle_type].append(dset)
                    else:
                        dataset_type_dict[particle_type] = [dset]
                else:
                    if REAL_DATA_ID in dataset_type_dict:
                        dataset_type_dict[REAL_DATA_ID].append(dset)
                    else:
                        dataset_type_dict[REAL_DATA_ID] = [dset]

            # set the number of events for each particle type (max_events is defined in experiment setting)
            # this allows to vary the proportion of gamma vs proton
            for type, dset in dataset_type_dict.items():
                max_event = max_events[type] if type in max_events.keys() else max_events["default"]
                concat_datasets = ConcatDataset(dset)
                indices = torch.randperm(len(concat_datasets)).numpy()[:max_event]
                dataset_type_dict[type] = Subset(concat_datasets, indices)
                logger = logging.getLogger(__name__)
                logger.info(f"Particle of type {type} dataset length: {len(dataset_type_dict[type])}")

            return ConcatDataset(list(dataset_type_dict.values()))
        else:
            # in test mode: we can merge the tests datasets (setting in experiment setting)
            # this allows to have a single output file (to pass to further processing DL2->DL**)
            # but needs to be for each type of particle (proton/gamma/electron)
            if self.experiment.merge_test_datasets:
                dataset_type_dict = {}

                for dset in datasets:
                    if dset.simu:
                        particle_type = dset.dl1_params["mc_type"][0]

                        if particle_type in dataset_type_dict:
                            dataset_type_dict[particle_type].append(dset)
                        else:
                            dataset_type_dict[particle_type] = [dset]
                    else:
                        if "real_list" in dataset_type_dict:
                            dataset_type_dict["real_list"].append(dset)
                        else:
                            dataset_type_dict["real_list"] = [dset]

                return [ConcatDataset(dset) for dset in dataset_type_dict.values()]
            else:
                return datasets


class GLearnDomainAdaptationDataModule(GLearnDataModule):
    """GLearnDataModule that works with 2 domains: source and target files, used for domain adaptation."""

    def __init__(self, experiment):
        super().__init__(experiment)
        self.dataset_balancing = experiment.dataset_parameters.get("dataset_balancing", False)

    def get_dataset(self, train):
        max_files = self.experiment.train_files_max_number if train else self.experiment.test_files_max_number
        max_events = self.experiment.dataset_size if train else {}
        data_module_source = utils.fetch_data_module_settings(self.experiment, train=train, domain="source")
        data_module_target = utils.fetch_data_module_settings(self.experiment, train=train, domain="target")
        source_datasets = self.get_glearn_dataset_from_path(
            data_module_source,
            train,
            domain="source",
            max_files=max_files,
            max_events=max_events.get("source", None) if max_events is not None else None,
        )
        target_datasets = self.get_glearn_dataset_from_path(
            data_module_target,
            train,
            domain="target",
            max_files=max_files,
            max_events=max_events.get("target", None) if max_events is not None else None,
        )

        if self.dataset_balancing:
            source_datasets, target_datasets = balance_datasets(source_datasets, target_datasets)
        else:
            source_datasets, target_datasets = shuffle_datasets(source_datasets, target_datasets)

        return GlearnDomainAdaptationDataset(source_datasets, target_datasets)
