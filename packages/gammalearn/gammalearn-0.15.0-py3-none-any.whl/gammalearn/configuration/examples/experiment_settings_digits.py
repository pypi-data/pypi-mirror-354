import collections
from pathlib import Path

import torch
from torch.optim import lr_scheduler
from torchmetrics.classification import Accuracy
from torchvision import transforms

import gammalearn.optimizers as optimizers
import gammalearn.training_steps as training_steps
from gammalearn.data.digit.digit_data_module import VisionDataModule
from gammalearn.data.digit.digit_dataset import DigitMixDataset
from gammalearn.data.image_processing.noise_augmentation import AddGaussianNoise
from gammalearn.data.save_results.metrics import (
    WriteAccuracy,
    WriteConfusionMatrix,
)
from gammalearn.data.transforms import GLearnCompose
from gammalearn.nets.gammaphysnet import GammaPhysNet
from gammalearn.nets.residual_net import ResNetAttention

# Experiment settings
main_directory = str(Path.home()) + "/gammalearn_experiments"  # TODO change directory if needed
"""str: mandatory, where the experiments are stored"""
project = "test_project"
"""str: optional, the name of the project."""
experiment_name = "test_install"
"""str: mandatory, the name of the experiment. Should be different
for each experiment, except if one wants to resume an old experiment
"""
tags = ["test_tags"]
"""list of str: optional, the tags of the experiment. Will be displayed in the wandb dashboard"""
info = ""
"""str: optional"""
gpus = 1
"""int or list: mandatory, the number of gpus to use. If -1, run on all GPUS, 
if None/0 run on CPU. If list, run on GPUS of list.
"""
log_every_n_steps = 1
"""int: optional, the interval in term of iterations for on screen
data printing during experiment. A small value may lead to a very large log file size.
"""
checkpointing_options = dict(every_n_epochs=1, save_top_k=3, save_last=True)
"""dict: optional, specific options for model checkpointing.
See https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.callbacks.ModelCheckpoint.html 
for details.
"""
random_seed = 1
"""int: optional, the manual seed to make experiments more reproducible"""
monitor_device = True
"""bool: optional, whether or not monitoring the gpu utilization"""
targets = collections.OrderedDict(
    {
        "class": {
            "label_shape": 1,
            "output_shape": 10,
            "loss": torch.nn.CrossEntropyLoss(),
            "loss_weight": 1,
            "metrics": {
                "Accuracy_digit": Accuracy(threshold=0.5),
            },
            "mt_balancing": False,
        },
    }
)
"""dict: mandatory, defines for every objectives of the experiment
the loss function and its weight
"""

dataset_class = DigitMixDataset
"""Dataset: mandatory, the Dataset class to load the data. Currently 2 classes are available, MemoryLSTDataset that 
loads images in memory, and FileLSTDataset that loads images from files during training.
"""
dataset_parameters = {
    "targets": list(targets.keys()),
}
"""dict: mandatory, the parameters of the dataset."""
preprocessing_workers = 4
"""int: optional, the max number of workers to create dataset."""
dataloader_workers = 4
"""int: optional, the max number of workers for the data loaders. If 0, data are loaded from the main thread."""
mp_start_method = "fork"
"""str: optional, the method to start new process in [fork, spawn]"""

net_parameters_dic = {
    "model": GammaPhysNet,
    "parameters": {
        "backbone": {
            "model": ResNetAttention,
            "parameters": {
                "num_layers": 3,
                "initialization": (torch.nn.init.kaiming_uniform_, {"mode": "fan_out"}),
                "normalization": (torch.nn.BatchNorm2d, {}),
                "num_channels": 3,
                "block_features": [4, 6, 8],
                # 'attention_layer': (DualAttention, {'ratio': 8}),
                "non_linearity": (torch.nn.ReLU, {}),
                "output_size": (5, 5),
            },
        },
        "fc_width": 32,
        "non_linearity": (torch.nn.ReLU, {}),
        "last_bias_init": None,
        "targets": {"class": 10},
    },
}

"""dict: mandatory, the parameters of the network. Depends on the
network chosen. Must include at least a model and a parameters field.
"""
# checkpoint_path = main_directory + '/test_install/checkpoint_epoch=0.ckpt'
"""str: optional, the path where to find the backup of the model to resume"""

profiler = None
# profiler = {'profiler': SimpleProfiler,
#             'options': dict(extended=True)
#             }
"""str: optional, the profiler to use"""

#########################################################################################
train = True
"""bool: mandatory, whether or not to train the model"""
# Data settings
data_module_train = {
    "module": VisionDataModule,
    "paths": ["/home/michael/workspace/datasets/digits/mnist"],  # TODO fill your folder path
    "transform": GLearnCompose(
        [
            transforms.ToTensor(),
            AddGaussianNoise(0.0, 0.5),
        ]
    ),
    "target_transform": None,
}
"""paths->list: mandatory, the folders where to find the hdf5 data files"""
"""image_filter->dict: optional, the filter(s) to apply to the dataset at image level"""
"""event_filter->dict: optional, the filter(s) to apply to the dataset"""

validating_ratio = 0.2
"""float: mandatory, the ratio of data to create the validating set"""
split_by_file = False
"""bool: optional, whether to split data at the file level or at the data level"""
max_epochs = 1
"""int: mandatory, the maximum number of epochs for the experiment"""
batch_size = 2
"""int: mandatory, the size of the mini-batch"""

train_files_max_number = 100
"""int: optional, the max number of files to use for the dataset"""

pin_memory = True
"""bool: optional, whether or not to pin memory in dataloader"""

# Training settings
loss_options = {}
loss_balancing_options = {}
"""dict: mandatory, defines for every objectives of the experiment
the loss function and its weight
"""
loss_balancing = None
"""function: mandatory, the function to compute the loss"""
optimizer_dic = {
    "network": optimizers.load_adam,
}
"""dict: mandatory, the optimizers to use for the experiment.
One may want to use several optimizers in case of GAN for example
"""
optimizer_parameters = {
    "network": {
        "lr": 1e-3,
        "weight_decay": 1e-4,
    },
}
"""dict: mandatory, defines the parameters for every optimizers to use"""
# regularization = {'weight': 10}
"""dict: optional, regularization to use during the training process. See in optimizers.py for 
available regularization functions."""
experiment_hparams = {}
training_step = training_steps.get_training_step_mt(**experiment_hparams)
# training_step = steps.training_step_gradnorm

"""function: mandatory, the function to compute the training step"""
eval_step = training_steps.get_eval_step_mt(**experiment_hparams)
"""function: mandatory, the function to compute the validating step"""
check_val_every_n_epoch = 1
"""int: optional, the interval in term of epoch for validating the model"""
lr_schedulers = {
    "network": {
        lr_scheduler.ReduceLROnPlateau: {
            "factor": 0.1,
            "patience": 10,
        }
    },
}
"""dict: optional, defines the learning rate schedulers"""
# callbacks
training_callbacks = []
"""dict: list of callbacks
"""
######################################################################################
# Testing settings
test = True
"""bool: mandatory, whether or not to test the model at the end of training"""
data_module_test = {
    "module": VisionDataModule,
    "paths": ["/home/michael/workspace/datasets/digits/mnistm"],  # TODO fill your folder path
    "transform": transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    ),
    "target_transform": None,
}
"""
dict: optional, must at least contain a non-empty 'source':{'paths:[]'}
path->list of str: optional, the folders containing the hdf5 data files for the test
image_filter->dict: optional, filter(s) to apply to the test set at image level
event_filter->dict: optional, filter(s) to apply to the test set
"""

test_step = training_steps.get_test_step_mt()
"""function: mandatory, the function to compute the validating step"""
dl2_path = ""
"""str: optional, path to store dl2 files"""
test_dataset_parameters = {
    # 'subarray': [1],
}
"""dict: optional, the parameters of the dataset specific to the test operation."""
test_files_max_number = 100
"""int: optional, the max number of files to use for the dataset"""
test_batch_size = 2
"""int: optional, the size of the mini-batch for the test"""
test_callbacks = [
    WriteAccuracy(),
    WriteConfusionMatrix(),
]
"""dict: list of callbacks"""
