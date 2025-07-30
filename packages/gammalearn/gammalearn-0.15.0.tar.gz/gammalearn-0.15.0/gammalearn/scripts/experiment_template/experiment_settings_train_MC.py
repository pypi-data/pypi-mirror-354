import collections
from pathlib import Path
import torch
from torch.optim import lr_scheduler

from torchmetrics.classification import Accuracy, AUROC

import gammalearn.criterions as criterions
import gammalearn.optimizers as optimizers
import gammalearn.steps as steps
from gammalearn.callbacks import (LogGradientNorm, LogModelWeightNorm, LogModelParameters,
                                  LogUncertaintyTracker,
                                  LogReLUActivations, LogLinearGradient, WriteDL2Files)
import gammalearn.datasets as dsets
from gammalearn.data_handlers import GLearnDataModule
from gammalearn.constants import GAMMA_ID, PROTON_ID
import gammalearn.data.nets as nets


# Experiment settings
main_directory = "{main_directory}"
"""str: mandatory, where the experiments are stored"""
project = 'test_project'
"""str: optional, the name of the project."""
experiment_name = "{exp_name}"
"""str: mandatory, the name of the experiment. Should be different
for each experiment, except if one wants to resume an old experiment
"""
tags = ['test_tags']
"""list of str: optional, the tags of the experiment. Will be displayed in the wandb dashboard"""
info = ''
"""str: optional"""
gpus = 1
"""int or list: mandatory, the number of gpus to use. If -1, run on all GPUS, 
if None/0 run on CPU. If list, run on GPUS of list.
"""
log_every_n_steps = 5
"""int: optional, the interval in term of iterations for on screen
data printing during experiment. A small value may lead to a very large log file size.
"""
window_size = 100
"""int: optional, the interval in term of stored values for metric moving computation"""
checkpointing_options = dict(every_n_epochs=1, save_top_k=-1, save_last=True)
"""dict: optional, specific options for model checkpointing.
See https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.callbacks.ModelCheckpoint.html 
for details.
"""
random_seed = 1
"""int: optional, the manual seed to make experiments more reproducible"""
monitor_device = True
"""bool: optional, whether or not monitoring the gpu utilization"""
particle_dict = {GAMMA_ID: 0,
                 PROTON_ID: 1,
                 # ELECTRON_ID: 2,
                 }
"""particle_dict is mandatory and maps cta particle types with class id. e.g. gamma (0) is class 0"""
targets = collections.OrderedDict({
    'energy': {
        'output_shape': 1,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {
            # 'functions': ,
        },
        'mt_balancing': True
    },
    'impact': {
        'output_shape': 2,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {},
        'mt_balancing': True
    },
    'direction': {
        'output_shape': 2,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {},
        'mt_balancing': True
    },
    'class': {
        'label_shape': 1,
        'output_shape': len(particle_dict),
        'loss': torch.nn.CrossEntropyLoss(label_smoothing=0.1),
        'loss_weight': 1,
        'metrics': {
            'Accuracy_particle': Accuracy(threshold=0.5, task="multiclass", num_classes=len(particle_dict)),
            'AUC_particle': AUROC(task="multiclass",
                                  num_classes=len(particle_dict)
                                  )
        },
        'mt_balancing': True
    }
})
"""dict: mandatory, defines for every objectives of the experiment
the loss function and its weight
"""

dataset_class = dsets.MemoryLSTDataset
# dataset_class = dsets.FileLSTDataset
"""Dataset: mandatory, the Dataset class to load the data. Currently 2 classes are available, MemoryLSTDataset that 
loads images in memory, and FileLSTDataset that loads images from files during training.
"""
dataset_parameters = {
    'camera_type': 'LST_LSTCam',
    'group_by': 'image',
    'use_time': True,
    'particle_dict': particle_dict,
    'targets': list(targets.keys()),
    # 'subarray': [1],
    'use_cleaning_masks': False,
}
"""dict: mandatory, the parameters of the dataset.
camera_type is mandatory and can be:
'LST_LSTCam', 'MST_NectarCam', 'MST_FlashCam', 'SST_ASTRICam', 'SST1M_DigiCam', 'SST_CHEC', 'MST-SCT_SCTCam'.
group_by is mandatory and can be 'image', 'event_all_tels', 'event_triggered_tels'.
particle_dict is mandatory and maps cta particle types with class id. e.g. gamma (0) is class 0, 
proton (101) is class 1 and electron (1) is class 2.
use_time (optional): whether or not to use time information
subarray (optional): the list of telescope ids to select as a subarray
use_cleaning_masks (boolean): whether to apply the cleaning mask to images and/or time (depending on use_time settings)
"""
preprocessing_workers = 4
"""int: optional, the max number of workers to create dataset."""
dataloader_workers = 4
"""int: optional, the max number of workers for the data loaders. If 0, data are loaded from the main thread."""
mp_start_method = 'fork'
"""str: optional, the method to start new process in [fork, spawn]"""

# Net settings
# Uncomment following lines to import your network from an external file
# net_definition_file = utils.nets_definition_path()
# """str: mandatory, the file where to find the net definition to use"""
# # Load the network definitions module #
# spec = importlib.util.spec_from_file_location("nets", net_definition_file)
# nets = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(nets)

net_parameters_dic = {
    'model': nets.GammaPhysNet,
    'parameters': {
        'backbone': {
            'model': nets.ResNetAttentionIndexed,
            'parameters': {
                'num_layers': 3,
                'initialization': (torch.nn.init.kaiming_uniform_, {'mode': 'fan_out'}),
                'normalization': (torch.nn.BatchNorm1d, {}),
                'num_channels': 2,
                'block_features': [16, 32, 64],
                'attention_layer': (nets.DualAttention, {'ratio': 16}),
                # 'attention_layer': (nets.SqueezeExcite, {'ratio': 4}),
                # 'attention_layer': None,
                'non_linearity': (torch.nn.ReLU, {}),
            }
        },
        'fc_width': 256,
        'non_linearity': (torch.nn.ReLU, {}),
        'last_bias_init': None,
        'targets': {k: v.get('output_shape', 0) for k, v in targets.items()}
    }
}
"""dict: mandatory, the parameters of the network. Depends on the
network chosen. Must include at least a model and a parameters field.
"""
# checkpoint_path = main_directory + '/test_install/checkpoint_epoch=3.ckpt'
"""str: optional, the path where to find the backup of the model to resume"""

profiler = None
# profiler = {'profiler': SimpleProfiler,
#             'options': dict(extended=True)
#             }
"""str: optional, the profiler to use"""

######################################################################################################################
train = True
"""bool: mandatory, whether or not to train the model"""
# Data settings
data_module_train = {
    'module': GLearnDataModule,
        'paths': [
            Path(__file__).parent.absolute().joinpath('../../../share/data/MC_data').resolve().as_posix(),
        ], # TODO fill your folder path
        'image_filter': {
            # utils.intensity_filter: {'intensity': [50, np.inf]},
            # utils.cleaning_filter: {'picture_thresh': 6, 'boundary_thresh': 3,
            #                         'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2},
            # utils.leakage_filter: {'leakage2_cut': 0.2, 'picture_thresh': 6, 'boundary_thresh': 3,
            #                        'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2},
        },
        'event_filter': {
            # utils.energyband_filter: {'energy': [0.02, 2], 'filter_only_gammas': True},  # in TeV
            # utils.emission_cone_filter: {'max_angle': 0.0698},
            # utils.impact_distance_filter: {'max_distance': 200},
            # utils.telescope_multiplicity_filter: {'multiplicity': 2},
        },
        'transform': None,
        'target_transform': None
}
"""paths->list: mandatory, the folders where to find the hdf5 data files"""
"""image_filter->dict: optional, the filter(s) to apply to the dataset at image level"""
"""event_filter->dict: optional, the filter(s) to apply to the dataset"""

validating_ratio = 0.2
"""float: mandatory, the ratio of data to create the validating set"""
max_epochs = 1
"""int: mandatory, the maximum number of epochs for the experiment"""
batch_size = 2
"""int: mandatory, the size of the mini-batch"""

# train_files_max_number = 1
"""int: optional, the max number of files to use for the dataset"""

pin_memory = True
"""bool: optional, whether or not to pin memory in dataloader"""


# Training settings
loss_options = {
    'conditional': True,
    'gamma_class': dataset_parameters['particle_dict'][0],
}
loss_balancing_options = {
    'log_var_coefficients': [2, 2, 2, 0.5],  # for uncertainty
    'penalty': 0,  # for uncertainty
}
"""dict: mandatory, defines for every objectives of the experiment
the loss function and its weight
"""
loss_balancing = criterions.UncertaintyWeighting(targets, **loss_balancing_options)
"""function: mandatory, the function to compute the loss"""
optimizer_dic = {
    # 'network': optimizers.load_sgd,
    'network': optimizers.load_adam,
    'loss_balancing': optimizers.load_adam
}
"""dict: mandatory, the optimizers to use for the experiment.
One may want to use several optimizers in case of GAN for example
"""
optimizer_parameters = {
    'network': {'lr': 1e-2,
                'weight_decay': 1e-7,
                # 'momentum': 0.9,
                # 'nesterov': True
                },
    'loss_balancing': {'lr': 0.025,
                       'weight_decay': 1e-4,
                       },
}
"""dict: mandatory, defines the parameters for every optimizers to use"""
# regularization = {'function': 'gradient_penalty',
#                   'weight': 10}
"""dict: optional, regularization to use during the training process. See in optimizers.py for 
available regularization functions. If `function` is set to 'gradient_penalty', the training step must be 
`training_step_mt_gradient_penalty`."""
experiment_hparams = {}
training_step = steps.get_training_step_mt(**experiment_hparams)
# training_step = steps.training_step_gradnorm
# training_step = steps.training_step_mt_gradient_penalty
"""function: mandatory, the function to compute the training step"""
eval_step = steps.get_eval_step_mt(**experiment_hparams)
"""function: mandatory, the function to compute the validating step"""
check_val_every_n_epoch = 1
"""int: optional, the interval in term of epoch for validating the model"""
lr_schedulers = {
    'network': {
        lr_scheduler.StepLR: {
            'gamma': 0.1,
            'step_size': 10,
        }
    },
    # 'network': {
    #     lr_scheduler.ReduceLROnPlateau: {
    #         'factor': 0.1,
    #         'patience': 30,
    #     }
    # },
    # 'network': {
    #     lr_scheduler.MultiStepLR: {
    #         'gamma': 0.1,
    #         'milestones': [10, 15, 18],
    #     }
    # },
    # 'network': {
    #     lr_scheduler.ExponentialLR: {
    #         'gamma': 0.9,
    #     }
    # },
}
"""dict: optional, defines the learning rate schedulers"""
# callbacks
training_callbacks = [
    LogGradientNorm(),
    LogModelWeightNorm(),
    LogModelParameters(),
    LogUncertaintyTracker(),
    # LogGradNormWeights(),
    LogReLUActivations(),
    LogLinearGradient(),
    # LogFeatures(),  # Do not use during training !! Very costly !!
]
"""dict: list of callbacks
"""

######################################################################################################################
# Testing settings
test = True
"""bool: mandatory, whether or not to test the model at the end of training"""
merge_test_datasets = False
"""bool: optional, whether or not to merge test datasets"""
data_module_test = {
    'module': GLearnDataModule,
        'paths': [
            Path(__file__).parent.absolute().joinpath('../../../share/data/MC_data').resolve().as_posix(),
        ],
        'image_filter': {
            # utils.intensity_filter: {'intensity': [10, np.inf]},
        # # utils.cleaning_filter: {'picture_thresh': 6, 'boundary_thresh': 3,
        # #                         'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2},
            # utils.leakage_filter: {'leakage2_cut': 0.2, 'picture_thresh': 6, 'boundary_thresh': 3,
            #                        'keep_isolated_pixels': False, 'min_number_picture_neighbors': 2},
        },
        'event_filter': {
            # utils.energyband_filter: {'energy': [0.02, 2], 'filter_only_gammas': True},  # in TeV
            # utils.emission_cone_filter: {'max_angle': 0.0698},
            # utils.impact_distance_filter: {'max_distance': 200},
            # utils.telescope_multiplicity_filter: {'multiplicity': 2},
        },
        'transform': None,
        'target_transform': None
}
"""
dict: optional, must at least contain a non-empty 'source':{'paths:[]'}
path->list of str: optional, the folders containing the hdf5 data files for the test
image_filter->dict: optional, filter(s) to apply to the test set at image level
event_filter->dict: optional, filter(s) to apply to the test set
"""

test_step = steps.get_test_step_mt(**experiment_hparams)
"""function: mandatory, the function to compute the validating step"""
dl2_path = ''
"""str: optional, path to store dl2 files"""
test_dataset_parameters = {
    # 'subarray': [1],
}
"""dict: optional, the parameters of the dataset specific to the test operation."""
test_batch_size = 2
"""int: optional, the size of the mini-batch for the test"""
test_callbacks = [
    WriteDL2Files()
]
"""dict: list of callbacks"""
