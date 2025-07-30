import logging

import torch
from lightning import LightningModule
import torchmetrics

from gammalearn.nets.utils import compute_total_parameter_number


class LitGLearnModule(LightningModule):
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment
        self.console_logger = logging.getLogger(__name__)
        self.grad_norm = 0

        self.net = self.experiment.net_parameters_dic["model"](self.experiment.net_parameters_dic["parameters"])
        if self.local_rank == 0:
            self.console_logger.info("network parameters number : {}".format(compute_total_parameter_number(self.net)))
        
        self.train_metrics = torch.nn.ModuleDict()
        self.val_metrics = torch.nn.ModuleDict()
        for task, param in self.experiment.targets.items():
            self.train_metrics[task] = torchmetrics.MetricCollection(param["metrics"]) 
            self.val_metrics[task] = torchmetrics.MetricCollection(param["metrics"]).clone()         

        self.loss_balancing = self.experiment.loss_balancing
        self.test_data = {"output": [], "label": [], "dl1_params": []}

        # Set optimization to manual, as we access the multiple optimizers manually in the training step
        self.automatic_optimization = False

    def forward(self, x):
        return self.net(x)

    def reset_test_data(self):
        self.test_data = {"output": [], "label": [], "dl1_params": []}

    def training_step(self, batch, batch_idx):
        # Reset gradients
        optimizers = self.optimizers(use_pl_optimizer=True)
        if isinstance(optimizers, list):
            for optim in optimizers:
                optim.zero_grad()
        else:
            optimizers.zero_grad()

        if batch_idx == 0 and self.trainer.current_epoch == 0:
            self.console_logger.info(("Experiment running on {}".format(self.device)))  # TODO handle multi gpus
            if self.device.type == "cuda":
                self.console_logger.info("GPU name : {}".format(torch.cuda.get_device_name(self.device.index)))

        output, labels, loss_data, loss = self.experiment.training_step(self, batch)

        self.manual_backward(loss)

        norm = 0
        for param in list(filter(lambda x: x.grad is not None, self.net.parameters())):
            norm += param.grad.detach().norm(2) ** 2 
        self.grad_norm = norm ** (1.0 / 2)

        if isinstance(optimizers, list):
            for optim in optimizers:
                optim.step()
        else:
            optimizers.step()

        for task, metric_collection_for_task in self.train_metrics.items():
            if task in output and task in labels:
                metric_collection_for_task.update(output[task], labels[task])

        # Journalisation conditionnelle pour la console
        n_batches = len(self.trainer.train_dataloader)
        if (batch_idx + 1) % self.experiment.log_every_n_steps == 0:
            self.console_logger.info("Epoch[{}] Iteration[{}/{}]".format(self.current_epoch, batch_idx + 1, n_batches))
            # log losses
            for n, v in loss_data.items():
                self.console_logger.info("Training Loss " + n + " {}".format(v))
            # log other metrics (pour la console)
            for task, metric_collection_for_task in self.train_metrics.items():
                if task in output and task in labels:
                    # For console logging, we calculate the metrics on the current accumulated state.
                    # MetricCollection.compute() returns a dictionary of calculated values.
                    # Important: .compute() here does NOT reset the state of the collection,
                    # which is correct if the accumulation is done over the entire epoch for self.log.
                    computed_values = metric_collection_for_task.compute() 
                    for name, m_value in computed_values.items():
                        self.console_logger.info(f"Training {name} ({task}) {m_value.item()}") 

        self.log_dict({"Training/Loss_" + n: v for n, v in loss_data.items()}, on_step=False, on_epoch=True)

        training_loss = 0
        for v_loop in loss_data.values():
            training_loss += v_loop
        self.log("Loss_training", training_loss, on_step=False, on_epoch=True)
        self.log("Loss_weighted_training", loss.detach(), on_step=False, on_epoch=True)

        # log other metrics
        for task, metric_collection_for_task in self.train_metrics.items():
            if task in output and task in labels:
                # Log each metric object. Lightning will handle .compute() and .reset() at epoch boundaries.
                for metric_name, metric_obj in metric_collection_for_task.items():
                    self.log(f"Training/{metric_name}_{task}", metric_obj, on_step=False, on_epoch=True)

        return loss

    def on_train_epoch_end(self):
        # it is necessary to call the step of the lr_schedulers manually because we set self.automatic_optimization = False
        lr_schedulers = self.lr_schedulers()
        if lr_schedulers is not None:
            lr_schedulers = [lr_schedulers] if not isinstance(lr_schedulers, list) else lr_schedulers
            for scheduler in lr_schedulers:
                if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    scheduler.step(self.trainer.callback_metrics["Loss_validating"])
                else:
                    scheduler.step()

    def validation_step(self, batch, batch_idx):
        output, labels, loss_data, loss = self.experiment.eval_step(self, batch)
        # log losses
        self.log_dict({"Validating_Loss_" + n: v for n, v in loss_data.items()})
        val_loss = 0
        for n, v in loss_data.items():
            # self.console_logger.info('Validating ' + n + ' {}'.format(v))
            val_loss += v
        self.log_dict({"Loss_validating": val_loss})
        self.log("Loss_validating", loss.detach())
        self.log("Loss_weighted_validating", loss.detach())
        # Accumulate metrics
        for task, all_metrics in self.val_metrics.items():
            for name, metric in all_metrics.items():
                metric(output[task], labels[task])

    def on_validation_epoch_end(self):
        # TODO: check if this is still usefull now that we have wandb, no need to check console output
        self.console_logger.info("Epoch[{}] Validation]".format(self.current_epoch))
        # log metrics
        for task, all_metrics in self.val_metrics.items():
            for name, metric in all_metrics.items():
                m_value = metric.compute()
                self.log(name + "_validating", m_value)
                self.console_logger.info("Validating " + name + " {}".format(m_value))
                metric.reset()  # We have to reset bc we manually log the metrics here (to log them in console)

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        """Store test values in self.test_data so they can be written in files with the dl2 or other write callback"""
        outputs, labels, dl1_params = self.experiment.test_step(self, batch)
        self.test_data["output"].append(outputs)
        self.test_data["label"].append(labels)
        self.test_data["dl1_params"].append(dl1_params)

    def configure_optimizers(self):
        # TODO: in practice, we never use another optimizer for the network and the tasks
        optim_keys = self.experiment.optimizer_dic.keys()
        self.optim_keys = optim_keys
        if "network" in optim_keys:
            assert all(
                key not in optim_keys for key in ["feature", "classifier", "regressor"]
            ), "If you define an optimizer for the whole network, you cant also define one for a subpart of it."

        if "feature" in optim_keys:
            assert (
                "classifier" in optim_keys or "regressor" in optim_keys
            ), "You need an optimizer for every subparts of the net."

        optimizers = {}
        for key in self.experiment.optimizer_dic.keys():
            if key == "network":
                optimizers[key] = self.experiment.optimizer_dic[key](
                    self.net, self.experiment.optimizer_parameters[key]
                )
            elif key == "loss_balancing":
                assert isinstance(self.experiment.loss_balancing, torch.nn.Module)
                optimizers[key] = self.experiment.optimizer_dic[key](
                    self.experiment.loss_balancing, self.experiment.optimizer_parameters[key]
                )
            else:
                # TODO: this in particular is never used (use an optimizer on something else than the network or task)
                try:
                    assert getattr(self.net, key, None) is not None
                except AssertionError as e:
                    self.console_logger.error(e)
                    print(key)
                    print(self.net)
                    raise e
                optimizers[key] = self.experiment.optimizer_dic[key](
                    getattr(self.net, key), self.experiment.optimizer_parameters[key]
                )

        # Configure schedulers as well
        if self.experiment.lr_schedulers is not None:
            schedulers = []
            for net_param, scheduler_param in self.experiment.lr_schedulers.items():
                for scheduler, params in scheduler_param.items():
                    if optimizers[net_param] is not None:
                        schedulers.append(
                            {
                                "scheduler": scheduler(optimizers[net_param], **params),
                                "name": "lr_" + net_param,
                            }
                        )
        else:
            schedulers = None

        return list(optimizers.values()), schedulers
