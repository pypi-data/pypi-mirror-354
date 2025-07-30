import torch
from lightning import Callback

import gammalearn.criterion.loss_balancing.grad_norm
import gammalearn.criterion.loss_balancing.loss_balancing
from gammalearn.criterion.loss_balancing.loss_weight_scheduler import BaseW
from gammalearn.criterion.loss_balancing.uncertainty_weighting import UncertaintyWeighting


class LogLambda(Callback):
    """
    Callback to send loss the gradient weighting from BaseW to logger
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        log_lambda_loss_dict, log_lambda_grad_dict = {}, {}
        targets = pl_module.experiment.loss_balancing.targets.copy()
        trainer = pl_module.trainer

        for i, task in enumerate(targets.keys()):
            if targets[task].get("loss_weight", None) is not None:
                if isinstance(targets[task]["loss_weight"], BaseW):
                    log_lambda_loss_dict["Lambda loss " + task] = targets[task]["loss_weight"].get_weight(trainer)
            if targets[task].get("grad_weight", None) is not None:
                if isinstance(targets[task]["grad_weight"], BaseW):
                    log_lambda_grad_dict["Lambda grad " + task] = targets[task]["grad_weight"].get_weight(trainer)

        if log_lambda_loss_dict:
            pl_module.log_dict(log_lambda_loss_dict, on_epoch=False, on_step=True)
        if log_lambda_grad_dict:
            pl_module.log_dict(log_lambda_grad_dict, on_epoch=False, on_step=True)


class LogUncertaintyTracker(Callback):
    """
    Callback to send loss log vars and precisions of the Uncertainty estimation method to logger
    logs the loss balancing log_variance and precision
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if isinstance(pl_module.experiment.loss_balancing, UncertaintyWeighting):
            logvar_dict = pl_module.experiment.loss_balancing.log_vars
            log_logvar_dict = {}
            log_precision_dict = {}

            targets = pl_module.experiment.loss_balancing.targets.copy()

            for i, task in enumerate(targets.keys()):
                log_logvar_dict["Log_var_" + task] = logvar_dict[i].detach().cpu()
                log_precision_dict["Precision_" + task] = torch.exp(-logvar_dict[i].detach().cpu())

            pl_module.log_dict(log_logvar_dict, on_epoch=False, on_step=True)
            pl_module.log_dict(log_precision_dict, on_epoch=False, on_step=True)


class LogGradNormTracker(Callback):
    """
    Callback to send gradnorm (loss balancing algo) parameters to logger

    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if isinstance(pl_module.experiment.loss_balancing, gammalearn.criterion.loss_balancing.grad_norm.GradNorm):
            g_dict = pl_module.experiment.loss_balancing.tracker_g
            r_dict = pl_module.experiment.loss_balancing.tracker_r
            k_dict = pl_module.experiment.loss_balancing.tracker_k
            l_dict = pl_module.experiment.loss_balancing.tracker_l
            l0_dict = pl_module.experiment.loss_balancing.tracker_l0
            lgrad = pl_module.experiment.loss_balancing.tracker_lgrad
            log_g_dict, log_r_dict, _, log_k_dict, log_l_dict, log_l0_dict = {}, {}, {}, {}, {}, {}

            for task in r_dict.keys():
                log_g_dict["Gradient_norms_" + task] = g_dict[task].detach().cpu()
                log_r_dict["Inverse_training_rate_" + task] = r_dict[task].detach().cpu()
                log_k_dict["Constant_" + task] = k_dict[task].detach().cpu()
                log_l_dict["Loss_ratio_" + task] = l_dict[task].detach().cpu()
                log_l0_dict["L0_" + task] = l0_dict[task].detach().cpu()
            log_lgrad = lgrad.detach().cpu()

            pl_module.log_dict(log_g_dict, on_epoch=False, on_step=True)
            pl_module.log_dict(log_r_dict, on_epoch=False, on_step=True)
            pl_module.log_dict(log_k_dict, on_epoch=False, on_step=True)
            pl_module.log_dict(log_l_dict, on_epoch=False, on_step=True)
            pl_module.log_dict(log_l0_dict, on_epoch=False, on_step=True)
            pl_module.log("Lgrad", log_lgrad, on_epoch=False, on_step=True)


class LogLossWeighting(Callback):
    """
    Callback to send loss weight coefficients to logger
    Parameters
    ----------
    Returns
    -------
    """

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        if isinstance(
            pl_module.experiment.loss_balancing, gammalearn.criterion.loss_balancing.loss_balancing.MultiLossBalancing
        ):
            weights_dict = pl_module.experiment.loss_balancing.weights_dict
            log_weights_dict = {}
            for task in weights_dict.keys():
                log_weights_dict["Loss_weight_per_task_" + task] = weights_dict[task].detach().cpu()
            pl_module.log_dict(log_weights_dict, on_epoch=False, on_step=True)
