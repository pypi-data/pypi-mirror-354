import collections
import torch
from torch.optim import lr_scheduler

from torchmetrics.classification import Accuracy, AUROC

import gammalearn.criterions as criterions
import gammalearn.optimizers as optimizers
import gammalearn.steps as steps
from gammalearn.callbacks import (LogGradientNorm, LogUncertaintyTracker, LogLambda, LogGradientNormPerTask, LogLossWeighting, 
                                  LogGradientCosineSimilarity, WriteDL2Files)
import gammalearn.utils as utils
import gammalearn.datasets as dsets
from gammalearn.data_handlers import GLearnDataModule
from gammalearn.constants import GAMMA_ID, PROTON_ID, SOURCE, TARGET
import gammalearn.data.nets as nets










# Experiment settings
main_directory = "/uds_data/glearn/Data/experiments"
"""str: mandatory, where the experiments are stored"""
project = "pointing_study"
"""str: optional, the name of the project."""
experiment_name = "PCBN_001"
"""str: mandatory, the name of the experiment. Should be different
for each experiment, except if one wants to resume an old experiment
"""
tags = ["pointing", "CBN", "training"]
"""list of str: optional, the tags of the experiment. Will be displayed in the wandb dashboard"""
info = "pointing through CBN on dec_2276"

gpus = 3
"""int or list: mandatory, the number of gpus to use. If -1, run on all GPUS, 
if None/0 run on CPU. If list, run on GPUS of list.
"""
log_every_n_steps = 1
"""int: optional, the interval in term of iterations for on screen
data printing during experiment. A small value may lead to a very large log file size.
"""
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
domain_dict = {SOURCE: 1,
               TARGET: 0,
               }
"""domain_dict is optional and maps the domain with class id. e.g. source is class 1"""
targets = collections.OrderedDict({
    'energy': {
        'output_shape': 1,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {},
        'mt_balancing': True,
    },
    'impact': {
        'output_shape': 2,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {},
        'mt_balancing': True,
    },
    'direction': {
        'output_shape': 2,
        'loss': torch.nn.L1Loss(reduction='none'),
        'loss_weight': 1,
        'metrics': {},
        'mt_balancing': True,
    },
    'class': {
        'label_shape': 1,
        'output_shape': len(particle_dict),
        'loss': torch.nn.CrossEntropyLoss(),
        'loss_weight': 1,
        'metrics': {
            'Accuracy_particle': Accuracy(threshold=0.5),
            'AUC_particle': AUROC(pos_label=particle_dict[GAMMA_ID],
                                  num_classes=len(particle_dict),
                                  compute_on_step=True
                                  )
        },
        'mt_balancing': True
    },
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
    'domain_dict': domain_dict,
    'targets': list(targets.keys()),
    'use_pointing': True
    # 'dataset_balancing': False,
    # 'subarray': [1],
}
"""dict: mandatory, the parameters of the dataset.
camera_type is mandatory and can be:
'LST_LSTCam', 'MST_NectarCam', 'MST_FlashCam', 'SST_ASTRICam', 'SST1M_DigiCam', 'SST_CHEC', 'MST-SCT_SCTCam'.
group_by is mandatory and can be 'image', 'event_all_tels', 'event_triggered_tels'.
particle_dict is mandatory and maps cta particle types with class id. e.g. gamma (0) is class 0, 
proton (101) is class 1 and electron (1) is class 2.
use_time (optional): whether or not to use time information
subarray (optional): the list of telescope ids to select as a subarray
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
    'model': nets.ConditionalGammaPhysNet,
    'parameters': {
        'main_task': {
            'model': nets.GammaPhysNet,
            'parameters': {
                'backbone': {
                    'model': nets.ResNetAttention,
                    'parameters': {
                        'num_layers': 3,
                        'initialization': (torch.nn.init.kaiming_uniform_, {'mode': 'fan_out'}),
                        'normalization': (nets.CBN, {'input_size': 8}),
                        # 'normalization': (torch.nn.BatchNorm2d, {}),
                        'num_channels': 2,
                        'block_features': [16, 32, 64],
                        'attention_layer': (nets.DualAttention, {'ratio': 16}),
                        'non_linearity': (torch.nn.ReLU, {}),
                        'output_size': (14, 14)
                    }
                },
                'fc_width': 256,
                'non_linearity': (torch.nn.ReLU, {}),
                'last_bias_init': None,
                'targets': {k: v.get('output_shape', 0) for k, v in targets.items()}
            },
        },
        'conditional_task': {
            'model': nets.LinearEncoder,
            'parameters': {
                'num_layers': 1,
                'input_size': 2,
                'hidden_size': 8,
                'output_size': 8,  # Must be equal to the input_size of the CBN
                'initialization': (torch.nn.init.kaiming_uniform_, {'mode': 'fan_out'}),
                'non_linearity': (torch.nn.ReLU, {}),
                'normalization': (torch.nn.BatchNorm1d, {}),
            }
        },
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

# trainer logger
# trainer_logger = utils.TrainerWandbLogger(offline=False)
trainer_logger = utils.TrainerTensorboardLogger()
"""dict: optional, the logger to use for the experiment."""

######################################################################################################################
train = True
"""bool: mandatory, whether or not to train the model"""
# Data settings
data_module_train = {
    'module': GLearnDataModule,
    'paths': [
         "/uds_data/glearn/Data/MC_DL1_LST/AllSky/20221215_v0.9.12_base_prod/TrainingDataset/dec_2276",
           ],  # TODO fill your folder path
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
    'transform': dsets.GLearnCompose([
        dsets.AddPoissonNoise([0., 1.]),
        dsets.ResampleImage('bilinear_interpolation', (55, 55, 1)),
    ]),
    'target_transform': None
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
# train_files_max_number = {
#     'source': -1,
#     'target': [2, 1],
# }
"""int or dict: optional, the max number of files to use for the dataset"""
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
    'requires_gradients': True,
    'layer': 'feature.block2_layer3.conv_block.cv2.weight',
}
"""dict: mandatory, defines for every objectives of the experiment
the loss function and its weight
"""
loss_balancing = criterions.UncertaintyWeighting(targets, **loss_balancing_options)
"""function: mandatory, the function to compute the loss"""
optimizer_dic = {
    'network': optimizers.load_adam,
    'loss_balancing': optimizers.load_sgd
}
"""dict: mandatory, the optimizers to use for the experiment.
One may want to use several optimizers in case of GAN for example
"""
optimizer_parameters = {
    'network': {
        'lr': 1e-3,
        'weight_decay': 1e-4,
        # 'nesterov': True
    },
    'loss_balancing': {
        'lr': 1e-3,
        'weight_decay': 1e-4,
    },
}
"""dict: mandatory, defines the parameters for every optimizers to use"""
# regularization = {'function': 'gradient_penalty',
#                   'weight': 10}
"""dict: optional, regularization to use during the training process. See in optimizers.py for 
available regularization functions. If `function` is set to 'gradient_penalty', the training step must be 
`training_step_mt_gradient_penalty`."""
experiment_hparams = {"add_pointing": True}
"""dict: optional, the hyperparameters of the experiment"""
training_step = steps.get_training_step_mt(**experiment_hparams)
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
}
"""dict: optional, defines the learning rate schedulers"""
# callbacks
training_callbacks = [
    LogGradientNorm(),
    LogGradientNormPerTask(),
    LogGradientCosineSimilarity(),
    LogUncertaintyTracker(),
    LogLossWeighting(),
    LogLambda(),
]
"""dict: list of callbacks
"""

######################################################################################################################
# Testing settings
test = True
"""bool: mandatory, whether or not to test the model at the end of training"""
merge_test_datasets = True
"""bool: optional, whether or not to merge test datasets"""
data_module_test = {
    'module': GLearnDataModule,
    'paths': [
        "/uds_data/glearn/Data/MC_DL1_LST/AllSky/20221215_v0.9.12_base_prod/TestingDataset/node_theta_23.630_az_259.265_/"
    ],  # TODO fill your folder path
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
    'transform': dsets.GLearnCompose([
        dsets.AddPoissonNoise(0.46),
        dsets.ResampleImage('bilinear_interpolation', (55, 55, 1)),
    ]),
    'target_transform': None
}
"""
dict: optional, must at least contain a non-empty 'source':{'paths:[]'}
path->list of str: optional, the folders containing the hdf5 data files for the test
image_filter->dict: optional, filter(s) to apply to the test set at image level
event_filter->dict: optional, filter(s) to apply to the test set
"""
# test_files_max_number = 1
"""int: optional, the max number of files to use for the dataset"""
test_step = steps.get_test_step_mt(**experiment_hparams)
"""function: mandatory, the function to compute the validating step"""
dl2_path = ''
"""str: optional, path to store dl2 files"""
test_dataset_parameters = {
    'test_on_target': False,
    # 'subarray': [1],
}
"""dict: optional, the parameters of the dataset specific to the test operation."""
test_batch_size = 2
"""int: optional, the size of the mini-batch for the test"""
test_callbacks = [
    WriteDL2Files(),
]
"""dict: list of callbacks"""


