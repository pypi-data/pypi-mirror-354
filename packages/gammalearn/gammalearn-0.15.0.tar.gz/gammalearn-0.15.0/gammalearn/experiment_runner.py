#!/usr/bin/env python

from __future__ import division, print_function

import faulthandler
import inspect
import logging
import os
from pathlib import Path
import importlib.util

import torch

from gammalearn.configuration.constants import SOURCE, TARGET
from gammalearn.criterion.multitask import LossComputing
from gammalearn.data.digit.digit_data_module import VisionDataModule, VisionDomainAdaptationDataModule
from gammalearn.data.LST_data_module import GLearnDataModule, GLearnDomainAdaptationDataModule
from gammalearn.gl_logging.trainer_logger import TrainerLogger, TrainerTensorboardLogger
from gammalearn.experiment_paths import get_wandb_checkpoint_path
faulthandler.enable()


def check_particle_mapping(particle_dict):
    """Check that each value in the particle dict is unique"""
    assert len(particle_dict) == len(set(particle_dict.values())), "Each mc particle type must have its own class"


class Experiment(object):
    """Loads the settings of the experiment from the settings object,
    check them and defines default values for not specified ones.
    """

    def __init__(self, settings):
        """
        Parameters
        ----------
        settings : the object created from the settings.py import
        """
        self._logger = logging.getLogger(__name__)
        self.hooks = {}
        self.camera_geometry = None

        ##################################################################################################
        # Experiment settings
        self._settings = settings

        # Load mandatory settings
        self._has_mandatory("main_directory", "where the experiments are stored")
        self._is_of_type("main_directory", str)
        self.main_directory = settings.main_directory

        self._has_mandatory("experiment_name", "the name of the experiment !")
        self._is_of_type("experiment_name", str)
        self.experiment_name = settings.experiment_name

        self.checkpointing_options = dict(
            dirpath=os.path.join(self.main_directory, self.experiment_name),
            monitor="Loss_validating",
            filename="checkpoint_{epoch}",
            every_n_epochs=1,
            save_top_k=-1,
        )

        self._has_mandatory(
            "gpus",
            "the gpus to use. If -1, run on all GPUS, if None/0 run on CPU. If list, run on GPUS of list.",
        )
        assert (
            isinstance(getattr(settings, "gpus"), (int, list)) or getattr(settings, "gpus") is None
        ), "CUDA device id must be int, list of int or None !"
        if not torch.cuda.is_available() and settings.gpus not in [None, 0]:
            self._logger.warning("Experiment requested to run on GPU, but GPU not available. Run on CPU")
            self.gpus = None
        elif settings.gpus == 0:
            self.gpus = None
        else:
            self.gpus = settings.gpus
        self.accelerator = "gpu" if self.gpus not in [0, None] else "auto"
        self.strategy = "ddp" if self.gpus not in [0, None] else "auto"

        self._has_mandatory("dataset_class", "the class to load the data")
        self.dataset_class = settings.dataset_class

        self._has_mandatory("dataset_parameters", "the parameters of the dataset (camera type, group by option...)")
        self.dataset_parameters = settings.dataset_parameters
        if "particle_dict" in self.dataset_parameters:
            check_particle_mapping(self.dataset_parameters["particle_dict"])
        if "domain_dict" not in self.dataset_parameters:
            self.dataset_parameters["domain_dict"] = {SOURCE: 1, TARGET: 0}

        self._has_mandatory("targets", "the targets to reconstruct")
        self.targets = settings.targets
        self.settings_file_path = None

        # Net settings
        self._has_mandatory("net_parameters_dic", "the parameters of the net described by a dictionary")
        assert isinstance(getattr(settings, "net_parameters_dic"), dict), "The net parameters must be a dict !"
        self.net_parameters_dic = settings.net_parameters_dic

        self._has_mandatory("train", "whether to test the model after training")
        self._is_of_type("train", bool)
        self.train = settings.train

        self._has_mandatory("test", "whether to test the model after training")
        self._is_of_type("test", bool)
        if settings.test and self.gpus is not None:
            if self.gpus > 1:
                self._logger.warning(
                    "Test is set to True and number of GPUs greater than 1, which is incompatible. \n \
                                     Test set to False. You will have to launch another job with maximum 1 GPU."
                )
                self.test = False
            else:
                self.test = settings.test
        else:
            self.test = settings.test

        # Optional experiments settings
        if hasattr(settings, "entity"):
            self._is_of_type("entity", str)
            self.entity = settings.entity
        else:
            self.entity = "gammalearn"

        if hasattr(settings, "project"):
            self._is_of_type("project", str)
            self.project = settings.project
        else:
            self.project = "default"

        if hasattr(settings, "info"):
            self._is_of_type("info", str)
            self.info = settings.info
        else:
            self.info = None

        if hasattr(settings, "tags"):
            self._is_of_type("tags", list)
            self.tags = settings.tags
        else:
            self.tags = []

        if hasattr(settings, "log_every_n_steps"):
            self._is_positive("log_every_n_steps")
            self.log_every_n_steps = settings.log_every_n_steps
        else:
            self.log_every_n_steps = 100

        if hasattr(settings, "net_definition_file"):
            self.net_definition_file = settings.net_definition_file
        else:
            self.net_definition_file = None

        if hasattr(settings, "checkpointing_options"):
            assert isinstance(settings.checkpointing_options, dict)
            self.checkpointing_options.update(settings.checkpointing_options)

        if hasattr(settings, "random_seed"):
            self._is_of_type("random_seed", int)
            self.random_seed = settings.random_seed
        else:
            self.random_seed = None

        if hasattr(settings, "monitor_device"):
            self._is_of_type("monitor_device", bool)
            self.monitor_device = settings.monitor_device
        else:
            self.monitor_device = False

        if hasattr(settings, "data_transform"):
            self._is_of_type("data_transform", dict)
            self.data_transform = settings.data_transform
        else:
            self.data_transform = None

        if hasattr(settings, "preprocessing_workers"):
            self._is_of_type("preprocessing_workers", int)
            self.preprocessing_workers = max(settings.preprocessing_workers, 0)
        else:
            self.preprocessing_workers = 0

        if hasattr(settings, "dataloader_workers"):
            self._is_of_type("dataloader_workers", int)
            self.dataloader_workers = max(settings.dataloader_workers, 0)
        else:
            self.dataloader_workers = 0

        if hasattr(settings, "mp_start_method"):
            self._is_of_type("mp_start_method", str)
            try:
                assert settings.mp_start_method in ["fork", "spawn"]
            except AssertionError:
                self.mp_start_method = torch.multiprocessing.get_start_method()
            else:
                self.mp_start_method = settings.mp_start_method
        else:
            self.mp_start_method = torch.multiprocessing.get_start_method()

        if hasattr(settings, "checkpoint_path"):
            if 'wandb-registry-model' in settings.checkpoint_path:
                self._logger.info("Downloading model from wandb registry")
                self.checkpoint_path = get_wandb_checkpoint_path(checkpoint_path=settings.checkpoint_path,
                                                                 root=os.path.join(self.main_directory, self.experiment_name))
            else:
                self.checkpoint_path = settings.checkpoint_path
        else:
            self.checkpoint_path = None

        self.profiler = settings.profiler if hasattr(settings, "profiler") else None

        if hasattr(settings, "trainer_logger"):
            self._is_of_type("trainer_logger", TrainerLogger)
            self.trainer_logger = settings.trainer_logger
        else:
            self.trainer_logger = TrainerTensorboardLogger()

        self.context = {"train": None, "test": None}

        #################################################################################################
        # Train settings
        if self.train:
            # Data settings
            self._has_mandatory("data_module_train", "the training and validating data folders")
            self.data_module_train = settings.data_module_train
            self.context = self._check_data_module(self.data_module_train)

            self._has_mandatory("validating_ratio", "the ratio of data for validation")
            self.validating_ratio = settings.validating_ratio

            self._has_mandatory("max_epochs", "the maximum number of epochs")
            self.max_epochs = settings.max_epochs

            self._has_mandatory("batch_size", "the batch size")
            self._is_positive("batch_size")
            self.batch_size = settings.batch_size

            # Training settings
            self._has_mandatory("optimizer_parameters", "the optimizers parameters described as a dictionary")
            self.optimizer_parameters = settings.optimizer_parameters

            self._has_mandatory("optimizer_dic", "the optimizers described as a dictionary")
            self.optimizer_dic = settings.optimizer_dic

            self._has_mandatory("training_step", "the function for the training step")
            self._is_function("training_step", 2)
            self.training_step = settings.training_step

            self._has_mandatory("eval_step", "the function for the evaluation step")
            self._is_function("eval_step", 2)
            self.eval_step = settings.eval_step

            # Optional settings
            if hasattr(settings, "loss_balancing"):
                if settings.loss_balancing is not None:
                    self.loss_balancing = settings.loss_balancing
                else:
                    self.loss_balancing = lambda x, m: x
            else:
                self.loss_balancing = lambda x, m: x

            if hasattr(settings, "dataset_size"):
                self._is_of_type("dataset_size", dict)
                self.dataset_size = settings.dataset_size
            else:
                self.dataset_size = None

            if hasattr(settings, "train_files_max_number"):
                self._is_of_type("train_files_max_number", (int, dict, list))
                self.train_files_max_number = settings.train_files_max_number
            else:
                self.train_files_max_number = None

            if hasattr(settings, "pin_memory"):
                self._is_of_type("pin_memory", bool)
                self.pin_memory = settings.pin_memory
            else:
                self.pin_memory = False

            if hasattr(settings, "regularization"):
                self.regularization = settings.regularization
            else:
                self.regularization = None

            if hasattr(settings, "check_val_every_n_epoch"):
                self._is_positive("check_val_every_n_epoch")
                self.check_val_every_n_epoch = settings.check_val_every_n_epoch
            else:
                self.check_val_every_n_epoch = 1

            if hasattr(settings, "lr_schedulers"):
                self.lr_schedulers = settings.lr_schedulers
            else:
                self.lr_schedulers = None

            if hasattr(settings, "training_callbacks"):
                self.training_callbacks = settings.training_callbacks
            else:
                self.training_callbacks = []

        else:
            self.data_module_train = None
            self.validating_ratio = None
            self.max_epochs = 0
            self.batch_size = None
            self.loss_options = None
            self.loss_balancing = None
            self.optimizer_parameters = None
            self.optimizer_dic = None
            self.training_step = None
            self.eval_step = None
            self.dataset_size = None
            self.train_files_max_number = None
            self.pin_memory = False
            self.regularization = None
            self.check_val_every_n_epoch = 1
            self.lr_schedulers = None
            self.training_callbacks = []

        ########################################################################################################
        # Test settings
        if self.test:
            self._has_mandatory("test_step", "the test iteration")
            self._is_function("test_step", 2)
            self.test_step = settings.test_step

            if hasattr(settings, "merge_test_datasets"):
                self._is_of_type("merge_test_datasets", bool)
                self.merge_test_datasets = settings.merge_test_datasets
            else:
                self.merge_test_datasets = False

            if hasattr(settings, "test_dataset_parameters"):
                self._is_of_type("test_dataset_parameters", dict)
                self.test_dataset_parameters = settings.test_dataset_parameters
            else:
                self.test_dataset_parameters = None

            if hasattr(settings, "data_module_test") and settings.data_module_test is not None:
                self.data_module_test = settings.data_module_test
                self._check_data_module(self.data_module_test, train=False)
            else:
                self.data_module_test = None

            if hasattr(settings, "dl2_path"):
                self._is_of_type("dl2_path", str)
                self.dl2_path = settings.dl2_path
                if not self.dl2_path:
                    self.dl2_path = None
            else:
                self.dl2_path = None

            if hasattr(settings, "output_dir"):
                self._is_of_type("output_dir", str)
                self.output_dir = settings.output_dir
                if not self.output_dir:
                    self.output_dir = None
            else:
                self.output_dir = None

            if hasattr(settings, "output_file"):
                self._is_of_type("output_file", str)
                self.output_file = settings.output_file
                if not self.output_file:
                    self.output_file = None
            else:
                self.output_file = None

            if hasattr(settings, "test_batch_size"):
                self.test_batch_size = settings.test_batch_size
            elif self.batch_size is not None:
                self.test_batch_size = self.batch_size
            else:
                raise ValueError

            if hasattr(settings, "test_callbacks"):
                self.test_callbacks = settings.test_callbacks
            else:
                self.test_callbacks = []

            if hasattr(settings, "test_files_max_number"):
                self._is_of_type("test_files_max_number", int)
                self.test_files_max_number = settings.test_files_max_number
            else:
                self.test_files_max_number = None

        else:
            self.test_step = None
            self.data_module_test = None
            self.merge_test_datasets = False
            self.test_batch_size = None
            self.test_callbacks = []
            self.test_dataset_parameters = None

        if not hasattr(settings, "loss_options") or isinstance(settings.loss_options, type(None)):
            self.LossComputing = LossComputing(self.targets)
        else:
            self.LossComputing = LossComputing(self.targets, **settings.loss_options)

        try:
            assert not (self.data_module_train is None and self.data_module_test is None)
        except AssertionError as err:
            self._logger.exception("No data module has been provided. Set either a train or a test data module.")
            raise err

        if self.validating_ratio is not None:
            try:
                assert 0 < self.validating_ratio < 1
            except AssertionError as err:
                self._logger.exception("Validation ratio must belong to ]0,1[.")
                raise err

    def _has_mandatory(self, parameter, message):
        try:
            assert hasattr(self._settings, parameter)
        except AssertionError as err:
            self._logger.exception("Missing {param} : {msg}".format(param=parameter, msg=message))
            raise err

    def _is_positive(self, parameter):
        message = "Specification error on  {param}. It must be set above 0".format(param=parameter)
        try:
            assert getattr(self._settings, parameter) > 0
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _is_of_type(self, parameter, p_type):
        message = "Specification error on  {param}. It must be of type {type}".format(param=parameter, type=p_type)
        try:
            assert isinstance(getattr(self._settings, parameter), p_type)
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _is_function(self, parameter, n_args):
        message = "Specification error on  {param}. It must be a function of {n_args} args".format(
            param=parameter, n_args=n_args
        )
        try:
            assert inspect.isfunction(getattr(self._settings, parameter))
        except AssertionError as err:
            self._logger.exception(message)
            raise err
        try:
            assert len(inspect.getfullargspec(getattr(self._settings, parameter))[0]) == n_args
        except AssertionError as err:
            self._logger.exception(message)
            raise err

    def _check_data_module(self, data_module, train=True):
        """
        Check if the train or the test data module specified in the experiment setting file satisfy the required
        specifications.
        """
        if train:
            module_list = [
                VisionDomainAdaptationDataModule,
                GLearnDomainAdaptationDataModule,
                VisionDataModule,
                GLearnDataModule,
            ]
        else:  # Domain adaptation is only used in the train context
            module_list = [VisionDataModule, GLearnDataModule]

        message = "Specification error on  {module}. {context} data module must belong to {module_list}.".format(
            context="Train" if train else "Test", module=data_module["module"], module_list=module_list
        )
        try:
            assert data_module["module"] in module_list
        except AssertionError as err:
            self._logger.exception(message)
            raise err

        context = {"train": None, "test": None}
        # Domain adaptation
        if data_module["module"] in [VisionDomainAdaptationDataModule, GLearnDomainAdaptationDataModule]:
            context["train"] = "domain_adaptation"
            # No source will raise an error later
            data_module["source"] = data_module.get("source", {})

            # Target is not mandatory
            data_module["target"] = data_module.get("target", {})

            # Target path is not mandatory
            data_module["target"]["paths"] = data_module["target"].get("paths", [])

            # Filters are not mandatory
            data_module["source"]["image_filter"] = data_module["source"].get("image_filter", {})
            data_module["source"]["event_filter"] = data_module["source"].get("event_filter", {})
            data_module["target"]["image_filter"] = data_module["target"].get("image_filter", {})
            data_module["target"]["event_filter"] = data_module["target"].get("event_filter", {})

            self._check_data_module_path(data_module["source"]["paths"])
        # No domain adaptation
        elif data_module["module"] in [VisionDataModule, GLearnDataModule]:
            # Path is mandatory and will raise an error later if not set
            data_module["paths"] = data_module.get("paths", [])

            # Filters are not mandatory
            data_module["image_filter"] = data_module.get("image_filter", {})
            data_module["event_filter"] = data_module.get("event_filter", {})

            self._check_data_module_path(data_module["paths"])

        return context

    def _check_data_module_path(self, data_module_path):
        # Train (source) paths are mandatory for both train and test
        message = "Specification error on  {param}. It must non-empty".format(param="paths")
        try:
            assert data_module_path and isinstance(data_module_path, list)
        except AssertionError as err:
            self._logger.exception(message)
            raise err

def load_experiment(settings_file: Path) -> Experiment:
    spec = importlib.util.spec_from_file_location("settings", settings_file)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    experiment = Experiment(settings)
    experiment.settings_file_path = settings_file
    return experiment