import torch
import torch.nn as nn
from lightning import LightningModule

from gammalearn.criterion.loss_balancing.loss_balancing import MultiLossBalancing
from gammalearn.criterion.loss_balancing.loss_weight_scheduler import DistributionW


class OutOfBalancing(MultiLossBalancing):
    """
    Manual weighting of the loss when mt_balancing is set to False. These hyperparameters must be defined in the targets dictionary
    of the experiment setting file. This class is used in the LossComputing class to handle the weights that are out of the loss
    balancing scope. This class must not be used directly by the user.
    """

    def __init__(
        self,
        targets: dict[str, dict],
        requires_gradients: bool = False,
        layer: str = None,
    ) -> None:
        super().__init__(
            targets=targets,
            balancing=False,
            requires_gradients=requires_gradients,
            layer=layer,
        )
        self.weights = torch.Tensor([1.0] * len(self.targets))  # Equal 1. by default

    def _weights_compute(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        self.weights = self._weights_fetch(module)


class DomainConditionalLoss(nn.Module):
    """
    This class is used to define the conditional loss. The loss is weighted by a mask that is set to 1 if the label
    belongs to the domain class of interest, 0 otherwise.
    """

    def __init__(self, training_class: list = None):
        super().__init__()
        self.loss_domain_mask = None

        if training_class is not None:
            assert isinstance(training_class, list), (
                "training class parameter must be of type list, got {} " "instead".format(type(training_class))
            )
            for c in training_class:
                assert isinstance(c, int), "{} must be of type int, got {} instead".format(c, type(c))
            self.training_class = training_class
            self.domain_conditional = True
        else:
            self.training_class = None
            self.domain_conditional = False

    def set_mask(self, labels: torch.Tensor) -> None:
        """
        Update the domain loss mask.

        Parameters
        ----------
        labels: (torch.Tensor) The ground truth class labels.
        """
        self.loss_domain_mask = torch.Tensor([1 if x in self.training_class else 0 for x in labels])
        self.bs = int(self.loss_domain_mask.shape[0] / 2)

    def get_source_mask_idx(self) -> torch.Tensor:
        return self.loss_domain_mask[: self.bs].nonzero()

    def get_source_mask(self) -> torch.Tensor:
        mask = torch.zeros(self.bs)
        mask[self.get_source_mask_idx()] = 1
        return mask

    def get_target_mask_idx(self) -> torch.Tensor:
        return self.loss_domain_mask[self.bs :].nonzero()

    def get_target_mask(self) -> torch.Tensor:
        mask = torch.zeros(self.bs)
        mask[self.get_target_mask_idx()] = 1
        return mask


class LossComputing:
    def __init__(
        self,
        targets,
        conditional=False,
        gamma_class=None,
        path_distrib_weights: str = None,
    ):
        self.targets = targets.copy()

        self.conditional = conditional
        if self.conditional:
            assert "class" in self.targets, "The conditional loss is defined based on particle type"
            assert gamma_class is not None, "To mask loss, one must provide the class of gamma"

        self.gamma_class = gamma_class
        self.out_of_balancing = OutOfBalancing(targets)

        if path_distrib_weights is not None:
            self.distrib_weights = DistributionW(path_distrib_weights)
        else:
            self.distrib_weights = None

    def regularization(self, loss: dict, module: LightningModule) -> dict:
        if module.experiment.regularization is not None:
            loss += (
                module.experiment.regularization["function"](module.net) * module.experiment.regularization["weight"]
            )
        return loss

    def compute_loss(self, output, labels, module: LightningModule = None):
        loss = {}
        loss_data = {}

        if self.conditional:
            loss_mask = labels.get("class")
            loss_mask = loss_mask == self.gamma_class

        # 'targets' and 'output' must contain the same keys, but 'labels' may contain more elements, such as a domain
        # key referring to whether it belongs to the source and target datasets. Thus, we need to check if targets and
        # output keys are subset of the labels keys.
        assert (self.targets.keys() == output.keys()) and set(output.keys()).issubset(set(labels.keys())), (
            "All targets must have output and label but targets: {} \n outputs: {} " "\n labels: {}".format(
                self.targets.keys(), output.keys(), labels.keys()
            )
        )

        for k, v in self.targets.items():
            out = output[k]
            lab = labels[k]

            # Check dimensions
            if k in ["energy", "direction", "impact"]:
                assert out.ndim == lab.ndim, (
                    "output and label must have same number of dimensions for correct "
                    "loss computation but are {} and {}".format(out.ndim, lab.ndim)
                )
                out_shape = self.targets[k].get("output_shape")
                lab_shape = self.targets[k].get("label_shape", out_shape)

                assert (
                    out.shape[-1] == out_shape
                ), "{} output shape does not match settings, got {} instead of {}".format(k, out.shape[-1], out_shape)
                assert (
                    lab.shape[-1] == lab_shape
                ), "{} output shape does not match settings, got {} instead of {}".format(k, lab.shape[-1], lab_shape)

            # Compute class masked loss for domain adaptation
            if isinstance(v["loss"], DomainConditionalLoss):
                if v["loss"].domain_conditional:
                    v["loss"].set_mask(labels["domain_mask"])

            # Get loss
            loss_k = v["loss"](out, lab)

            # Apply weights based on distribution
            if self.distrib_weights is not None:
                if k in ["energy"]:
                    loss_k = self.distrib_weights.apply(loss_k, labels[k])

            # Compute class masked loss
            if k in ["energy", "direction", "impact"]:
                if self.conditional:
                    loss_mask = loss_mask.to(out.device)
                    assert loss_k.shape[0] == loss_mask.shape[0], (
                        "loss should not be reduced for mask on particle type" "but got {} and {}".format(
                            loss_k.shape, loss_mask.shape
                        )
                    )
                    if loss_k.dim() > 1:
                        cond = [loss_mask.unsqueeze(1) for _ in range(loss_k.shape[1])]
                        cond = torch.cat(cond, dim=1)
                    else:
                        cond = loss_mask
                    assert (
                        loss_k.shape == cond.shape
                    ), "loss and mask must have the same shape but are {} and {}".format(loss_k.shape, cond.shape)
                    loss_k = (
                        (loss_k * cond).sum() / cond.sum()
                        if cond.sum() > 0
                        else torch.tensor(0.0, device=loss_k.device)
                    )

            if k in ["autoencoder"]:
                loss_k = torch.mean(loss_k, dim=tuple(torch.arange(loss_k.dim())[1:]))
                loss_data[k] = loss_k.mean()
                loss[k] = loss_k.mean()
            else:
                loss_data[k] = loss_k.mean().detach().item()
                loss[k] = loss_k.mean()

        # Hand-designed loss weight. Requires to be out of the loss balancing scope.
        if len(self.out_of_balancing.targets) > 0:
            loss = self.out_of_balancing(loss, module)

        return loss, loss_data
