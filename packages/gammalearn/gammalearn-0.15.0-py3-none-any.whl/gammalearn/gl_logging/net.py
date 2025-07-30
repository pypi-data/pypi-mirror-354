import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torchvision.utils as t_utils
from astropy.table import Table
from ctapipe.instrument import CameraGeometry
from ctapipe.visualization import CameraDisplay
from indexedconv.utils import build_hexagonal_position, create_index_matrix, pool_index_matrix
from lightning import Callback
from lightning.pytorch.loggers import TensorBoardLogger, WandbLogger
from PIL import Image
from torchmetrics.functional.pairwise import pairwise_cosine_similarity
from torchvision import transforms
from pathlib import Path

import gammalearn.criterion.loss_balancing.loss_balancing as criterions
import wandb
import os 
import shutil
from gammalearn.data.utils import find_datafiles

def build_code_artifact(files_list) -> wandb.Artifact:
    """Build a wandb Artifact that contains scripts used to lauch the experiment.
    If the experiment is launched within an HTCondor Job, the artifact can contain multiple scripts 
    added with the env variable WANDB_LOG_FILES.
    
    Parameters
    ----------
        files_list (list): a list of path related to script files to be added to the code artifact of the run.

    Returns
    -------
        wandb.Artifact: An artifact ready to be logged that contains scripts added as files in the artifact.
    """
    code_artifact = wandb.Artifact(
        name="scripts",
        type="code",
        metadata={"files": files_list}
    )
    for filepath in files_list:
        code_artifact.add_file(filepath)
    return code_artifact

class LogWandb(Callback):
    """
    Callback to use training and testing datasets logged on wandb as input artifacts (train_dataset, test_dataset,
    model) and to log output artifacts (model, dl2) to the current project. Model artifact produced are also linked to the
    gammalearn model registry of wandb (https://wandb.ai/orgs/gammalearn-org/registry/model).
    At the end of training or testing stage, scripts related to the experiment are logged.

    Attributes
    ----------
    model_artifact_on_wandb (wandb.Artifact): Updated with artifact object if model artifact is logged on wandb during training or
        if model artifact is fetched from wandb's model registry in the :func:`get_wandb_checkpoint_path`, this attribute will be 
        equal to the wandb.Artifact object. None by default.
    """
    model_artifact_on_wandb = None

    def on_train_start(self, trainer, pl_module) -> None:
        """When training process is initialized, a train_dataset artifact is used. If the artifact's version  matches the latest one that 
        exists on wandb, the last artifact version is fetched otherwise it is created and logged to wandb.
        """
        if not any(isinstance(logger, WandbLogger) for logger in trainer.loggers):
            wandb.init(project=pl_module.experiment.project, 
                       entity="gammalearn",
                       name=f"{pl_module.experiment.experiment_name}_train",
                       tags=pl_module.experiment.tags,
                       notes=pl_module.experiment.info)
            
        #LOG TRAIN DATASET
        train_files_list = find_datafiles(pl_module.experiment.data_module_train['paths'], -1)
        train_files_list = list(train_files_list)
        train_dataset_artifact = wandb.Artifact(name="train_dataset",
                                                type="dataset",
                                                use_as="dataset",
                                                metadata={'local_paths': train_files_list}
                                                )
        for file in train_files_list:
            train_dataset_artifact.add_reference(uri=f"file:{file}", name=Path(file).name)
        
        wandb.use_artifact(train_dataset_artifact, type='dataset')

    def on_fit_end(self, trainer, pl_module) -> None:
        """At the end of training and validation processes, the checkpoint file is added as a file within the model artifact. Then
        model is logged on wandb's project and link to the wandb-registry-model/<wandb_project>. If wandb_project within the wandb-model-registry
        does not exist, it automatically creates the folder to save the checkpoint file.
        Log the scripts associated to the training run. If the environment variable called "LOG_WANDB_FILES" exists, 
        all the files saved in this variable will be logged.
        """
        #LOG MODEL
        checkpoint_path = Path(trainer.checkpoint_callback.last_model_path)
        model = wandb.Artifact(
            name="model",
            type="model",
            use_as="model",
            metadata={"path": checkpoint_path}
        )

        model.add_file(local_path=checkpoint_path)
        LogWandb.model_artifact_on_wandb = wandb.log_artifact(model).wait()
        wandb.run.link_artifact(model,f"wandb-registry-model/{pl_module.experiment.project}")  

        # LOG CODE
        scripts = [pl_module.experiment.settings_file_path]
        if os.getenv("WANDB_LOG_FILES") is not None:
            for file in os.getenv("WANDB_LOG_FILES").split(","):
                if Path(file).exists():
                    scripts.append(Path(file))
                    exp_dir = Path(pl_module.experiment.main_directory).joinpath(pl_module.experiment.experiment_name)
                    shutil.copy(Path(file), exp_dir)
        code_artifact = build_code_artifact(scripts)
        wandb.log_artifact(code_artifact).wait()

    def on_test_start(self, trainer, pl_module) -> None:
        """Create a new wandb test run that uses input artifacts (test_dataset and model). If test_dataset is not logged on wandb or if
        it is a new version, it logs it to wandb. Same for model checkpoint."""
        if wandb.run is not None:
            wandb.finish()
        
        wandb.init(project=pl_module.experiment.project, 
                   entity="gammalearn",
                   name=f"{pl_module.experiment.experiment_name}_test",
                   tags=pl_module.experiment.tags,
                   notes=pl_module.experiment.info)
        
        #LOG TEST DATASET
        test_files_list = find_datafiles(pl_module.experiment.data_module_test['paths'], -1)
        test_files_list = list(test_files_list)
        test_dataset_artifact = wandb.Artifact(name="test_dataset",
                                                type="dataset",
                                                use_as="dataset",
                                                metadata={'local_paths': test_files_list}
                                                )
        for file in test_files_list:
            test_dataset_artifact.add_reference(uri=f"file:{file}", name=Path(file).name)

        wandb.use_artifact(test_dataset_artifact) 

        #LOG MODEL
        if LogWandb.model_artifact_on_wandb is None:
            model_artifact = wandb.Artifact(name="model",
                                            type="model",
                                            use_as="model",
                                            metadata={"path": str(pl_module.experiment.checkpoint_path)}
                                            )
            model_artifact.add_file(local_path=pl_module.experiment.checkpoint_path)

        else:
            model_artifact = LogWandb.model_artifact_on_wandb

        wandb.use_artifact(model_artifact, type='model')

    def on_test_end(self, trainer, pl_module) -> None:
        """At the end of model testing, DL2 files are logged to wandb experiment as artifact.
        A unique artifact is created with no value in it : the artifact only contains references
        to the DL2 files (path and metadata such as file size). 
        Log the scripts associated to the test run. If the environment variable called "LOG_WANDB_FILES" exists, 
        all the files saved in this variable will be logged.
        """
        #LOG DL2
        if pl_module.experiment.data_module_test is None or pl_module.experiment.merge_test_datasets:
            output_dir = pl_module.experiment.main_directory + "/" + pl_module.experiment.experiment_name
        else:
            if pl_module.experiment.dl2_path is not None:
                output_dir = pl_module.experiment.dl2_path
            else:
                output_dir = pl_module.experiment.main_directory + "/" + pl_module.experiment.experiment_name + "/dl2/"

        dl2_files = list(Path(output_dir).glob("*.h5"))

        if len(dl2_files) > 0:
            dl2_artifact = wandb.Artifact(name="dl2",
                                        type="dl2",
                                        metadata={'local_paths': dl2_files})
            for file in dl2_files:
                dl2_artifact.add_reference(uri=f"file:{file}", 
                                        name=Path(file).name
                                        )
            wandb.log_artifact(dl2_artifact).wait()

        # LOG CODE
        scripts = [pl_module.experiment.settings_file_path]
        if os.getenv("WANDB_LOG_FILES") is not None:
            for file in os.getenv("WANDB_LOG_FILES").split(","):
                    if Path(file).exists():
                        scripts.append(Path(file))
                        exp_dir = Path(pl_module.experiment.main_directory).joinpath(pl_module.experiment.experiment_name)
                        shutil.copy(Path(file), exp_dir)
        code_artifact = build_code_artifact(scripts)
        wandb.log_artifact(code_artifact).wait()

class LogModelWeightNorm(Callback):
    """
    Callback to send sum of squared weigths of the network to logger
    Parameters
    ----------
    Returns
    -------

    """

    def on_train_epoch_end(self, trainer, pl_module):
        weights = 0
        for name, param in pl_module.net.named_parameters():
            if "weight" in name:
                weights += torch.sum(param.data**2)
        pl_module.log("weights", weights, on_epoch=True, on_step=False)


class LogModelParameters(Callback):
    """
    Callback to send the network parameters to logger

    Warning: doesn't work with wandb ? (too much data ?)
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_epoch_end(self, trainer, pl_module):
        if isinstance(pl_module.loggers, TensorBoardLogger):
            for name, param in pl_module.net.named_parameters():
                pl_module.logger.experiment.add_histogram(
                    name, param.detach().cpu(), bins="tensorflow", global_step=pl_module.current_epoch
                )
        else:
            # In that case, trainer_logger.watch is implemented in the experiment runner
            pass


def make_activation_sender(pl_module, name):
    """
    Creates the adapted activations sender to tensorboard

    TODO: Used only to log RELU activations. Remove ?
    not compatible with wandb

    Parameters
    ----------
    pl_module (LightningModule): the tensorboardX writer
    name (string) : name of the layer which activation is logged

    Returns
    -------
    An adapted function
    """

    def send(m, input, output):
        """
        The function to send the activation of a module to tensorboard
        Parameters
        ----------
        m (nn.Module): the module (eg nn.ReLU, ...)
        input
        output

        Returns
        -------

        """
        pl_module.logger.experiment.add_histogram(
            name, output.detach().cpu(), bins="tensorflow", global_step=pl_module.current_epoch
        )

    return send


class LogReLUActivations(Callback):
    """
    Callback to send activations layers output to logger

    doesn't work for wandb

    Parameters
    ----------
    Returns
    -------
    """

    def setup(self, trainer, pl_module, stage):
        self.hooks = []

    def on_train_epoch_start(self, trainer, pl_module):
        for name, child in pl_module.net.named_children():
            if isinstance(child, nn.ReLU):
                sender = make_activation_sender(pl_module, name)
                self.hooks.append(child.register_forward_hook(sender))

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        for hook in self.hooks:
            hook.remove()


def make_linear_gradient_logger(pl_module, name):
    def log_grad(m, grad_input, grad_output):
        pl_module.logger.experiment.add_histogram(
            name + "grad_in", grad_input[0].data.cpu(), bins="tensorflow", global_step=pl_module.current_epoch
        )

    return log_grad


class LogLinearGradient(Callback):
    """
    Callback to send gradients of the model to logger

    doesn't work with wandb, logs a lot of data

    Parameters
    ----------
    Returns
    -------
    """

    def setup(self, trainer, pl_module, stage):
        self.hooks = []

    def on_train_epoch_start(self, trainer, pl_module):
        for name, child in pl_module.net.named_modules():
            if isinstance(child, nn.Linear):
                grad_logger = make_linear_gradient_logger(pl_module, name)
                self.hooks.append(child.register_full_backward_hook(grad_logger))

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        for hook in self.hooks:
            hook.remove()


def make_feature_logger(pl_module, name, index_matrices):
    """Makes the function that logs the output of each layer of the model"""

    def log_features(m, input, output):
        if output.dim() == 3:
            features = output.detach().cpu().clone()
            images_list = []
            index_matrix = index_matrices[features.shape[-1]]
            pixel_pos = np.array(build_hexagonal_position(index_matrix.squeeze().squeeze()))
            pix_area = np.full(features.shape[-1], 6 / np.sqrt(3) * 0.5**2)
            # TODO load meta from datafile
            geom = CameraGeometry.from_table(
                Table(
                    {
                        "pix_id": np.arange(features.shape[-1]),
                        "pix_x": list(map(lambda x: x[0], pixel_pos)),
                        "pix_y": list(map(lambda x: x[1], pixel_pos)),
                        "pix_area": pix_area,
                    },
                    meta={
                        "PIX_TYPE": "hexagonal",
                        "PIX_ROT": 0,
                        "CAM_ROT": 0,
                    },
                )
            )

            for b, batch in enumerate(features):
                for c, channel in enumerate(batch):
                    label = "{}_b{}_c{}".format(name, b, c)
                    ax = plt.axes(label=label)
                    ax.set_aspect("equal", "datalim")
                    disp = CameraDisplay(geom, ax=ax)
                    disp.image = channel
                    disp.add_colorbar()
                    ax.set_title(label)
                    canvas = plt.get_current_fig_manager().canvas
                    canvas.draw()
                    pil_img = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
                    images_list.append(transforms.ToTensor()(pil_img))

            grid = t_utils.make_grid(images_list)

            pl_module.logger.experiment.add_image("Features_{}".format(name), grid, pl_module.current_epoch)

    return log_features


class LogFeatures(Callback):
    """logs the output of each layer of the model

    Warning: logs a LOT of data, so slows down considerably the training."""

    def setup(self, trainer, pl_module, stage):
        self.hooks = []
        self.index_matrices = {}
        index_matrix = create_index_matrix(
            pl_module.camera_parameters["nbRow"],
            pl_module.camera_parameters["nbCol"],
            pl_module.camera_parameters["injTable"],
        )
        n_pixels = int(torch.sum(torch.ge(index_matrix[0, 0], 0)).data)
        self.index_matrices[n_pixels] = index_matrix
        idx_matx = index_matrix
        while n_pixels > 1:
            idx_matx = pool_index_matrix(idx_matx, kernel_type=pl_module.camera_parameters["layout"])
            n_pixels = int(torch.sum(torch.ge(idx_matx[0, 0], 0)).data)
            self.index_matrices[n_pixels] = idx_matx

    def on_train_epoch_start(self, trainer, pl_module):
        """Register hooks to the `nn.ReLU` layers to log the output"""
        for name, child in pl_module.net.named_children():
            if isinstance(child, nn.ReLU):
                feature_logger = make_feature_logger(pl_module, name, self.index_matrices)
                self.hooks.append(child.register_forward_hook(feature_logger))

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        """Remove the hooks"""
        for hook in self.hooks:
            hook.remove()


class LogGradientNorm(Callback):
    """
    Callback to send the gradient total norm (gradient of the entire model) to logger

    Parameters
    ----------
    Returns
    -------
    """

    def on_train_epoch_end(self, trainer, pl_module):
        # the model total gradient (pl_module.grad_norm) is computed in the LitGlearnModule training step
        pl_module.log("Gradient_norm", pl_module.grad_norm, on_epoch=True, on_step=False)


class LogGradientCosineSimilarity(Callback):
    """
    Callback to send the tasks gradient cosine similarity to logger
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if isinstance(pl_module.experiment.loss_balancing, criterions.MultiLossBalancing):
            if pl_module.experiment.loss_balancing.requires_gradients:
                gradients = pl_module.experiment.loss_balancing.gradients
                similarity = pairwise_cosine_similarity(gradients, gradients)
                log_similarity_dict = {}
                targets = pl_module.experiment.targets.copy()
                for i, task_i in enumerate(targets):
                    for j, task_j in enumerate(targets):
                        if i < j:  # Only upper triangular matrix as similarity is symmetric
                            log_similarity_dict["Gradient_cosine_similarity_" + task_i + "_" + task_j] = similarity[
                                i, j
                            ]
                pl_module.log_dict(log_similarity_dict, on_epoch=False, on_step=True)


class LogGradientNormPerTask(Callback):
    """
    Callback to send the tasks gradient norm to logger
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if isinstance(pl_module.experiment.loss_balancing, criterions.MultiLossBalancing):
            if pl_module.experiment.loss_balancing.requires_gradients:
                gradients_dict = pl_module.experiment.loss_balancing.gradients_dict
                log_gradients_dict = {}
                for task in gradients_dict.keys():
                    log_gradients_dict["Gradient_norm_per_task_" + task] = (
                        gradients_dict[task].norm(p=2).detach().cpu()
                    )
                pl_module.log_dict(log_gradients_dict, on_epoch=False, on_step=True)
