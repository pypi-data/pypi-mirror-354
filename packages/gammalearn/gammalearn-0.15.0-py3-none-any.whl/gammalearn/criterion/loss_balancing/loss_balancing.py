import torch
import torch.nn as nn
from lightning import LightningModule
from gammalearn.criterion.loss_balancing.loss_weight_scheduler import BaseW


class GradientToolBox:
    """
    This class gathers some functions to calculate the gradients on a specified set of weights.
    Inspired from https://github.com/median-research-group/LibMTL/blob/main/LibMTL/weighting/abstract_weighting.py
    """

    def __init__(self, targets: dict[str, dict], layer: str = None) -> None:
        self.targets = targets.copy()
        self.num_targets = len(self.targets)
        self.layer = layer
        self.parameters = None

    def get_parameters(self):
        """
        Returns the parameters.
        """
        return self.parameters

    def set_parameters(self, module: nn.Module):
        """
        Set the parameters.
        """
        assert self.layer is not None, "The layer must be specified."
        model = module.net if isinstance(module, LightningModule) else module
        parameters = [(n, p) for n, p in model.named_parameters() if self.layer in n]
        assert parameters, "No parameters found for layer {}.".format(self.layer)

        _, self.parameters = parameters[-1]

    def initialize_gradients(self):
        return torch.zeros(self.num_targets, 1)

    def compute_gradients(self, loss: dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Compute the gradients on the set shared weights.
        """
        assert self.get_parameters() is not None, "The parameters must be set before computing the gradients."
        gradients = []
        for k in self.targets.keys():
            gradients.append(
                torch.autograd.grad(
                    outputs=loss[k],
                    inputs=self.get_parameters(),
                    retain_graph=True,  # Allows to use .backward() multiple times
                    create_graph=True,  # Allows to compute the gradients of the gradnorm weights
                    allow_unused=True,  # Allows to compute the gradients in the multi-task scenario
                )[0].flatten()
            )
        return torch.stack(gradients)


class MultiLossBalancing(nn.Module):
    """
    Generic function for loss balancing.

    Parameters
    ----------
    targets : dict
        The loss dictionary defining for every objective of the experiment the loss function

    Returns
    -------
    """

    def __init__(
        self,
        targets: dict[str, dict],
        balancing: bool = True,
        requires_gradients: bool = False,
        layer: str = None,
    ):
        super().__init__()
        if requires_gradients:
            assert layer is not None, "If requires_gradients is True, the layer must be specified."
        self.targets = targets.copy()
        self.weights = None
        self.weights_dict = {}  # To log using callbacks
        self.gradient = None
        self.gradients_dict = {}  # To log using callbacks
        self.requires_gradients = requires_gradients  # Whether to compute the gradients
        self.device = None
        self.layer = layer
        self.gtb = GradientToolBox(self.targets, layer) if self.requires_gradients else None
        self.gi = []  # Gradient indices

        for i, (k, v) in enumerate(targets.items()):
            if balancing:  # For automatic weighting strategy
                if not v.get("mt_balancing", False):  # Only keep targets with parameter 'mt_balancing' set to True
                    self.targets.pop(k)  # Discard it
                else:
                    self.gi.append(i)  # Keep it
            else:  # For manual weighting strategy
                if v.get("mt_balancing", False):  # Only keep targets with parameter 'mt_balancing' set to False
                    self.targets.pop(k)  # Discard it
                else:
                    pass  # Keep it

    def _set_device(self, loss: dict[str, torch.Tensor]) -> None:
        if self.device is None:
            self.device = next(iter(loss.values())).device

    def _set_layer(self, module: LightningModule) -> None:
        """
        Set the layer of the network from the given name.
        """
        if self.gtb is not None:
            self.gtb.set_parameters(module)

    def _setup(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        """
        Optional and method-dependent.
        """
        pass

    def _i(self, module: LightningModule) -> int:
        """
        The current iteration.
        """
        return module.trainer.fit_loop.total_batch_idx

    def _is_first_iter(self, module: LightningModule) -> bool:
        """
        Whether it is the first iteration of the training.
        """
        return self._i(module) == 0

    def _is_training(self, loss: dict[str, torch.Tensor]) -> bool:
        """
        Whether it is the training or the validation mode. During validation, the requires_grad attribute is set to False.
        """
        return all([loss_k.requires_grad for loss_k in loss.values()])

    def _weights_fetch(self, module: LightningModule) -> torch.Tensor:
        """
        Fetch the weights defined by the user.
        """
        weights = torch.Tensor(torch.ones(len(self.targets)))
        for i, v in enumerate(self.targets.values()):
            if v.get("loss_weight", None) is not None:
                if isinstance(v["loss_weight"], BaseW):
                    weights[i] = v["loss_weight"].get_weight(module.trainer)
                else:
                    weights[i] = v["loss_weight"]
        return weights

    def _weights_compute(self, loss: dict[str, torch.Tensor], module: LightningModule = None) -> None:
        """
        Mandatory and method-dependent.
        """
        return NotImplementedError

    def _weights_apply(self, loss: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = self.weights[i] * loss[k]

        return weighted_loss

    def _weights_update(self) -> None:
        for i, k in enumerate(self.targets.keys()):
            self.weights_dict[k] = self.weights[i].clone().detach()

    def _gradients_compute(self, loss: dict[str, torch.Tensor]) -> None:
        """
        Usually used to compute the gradients at the last shared layer. In that case, the gradients computed in the backbone are not calculted.
        Theoretically, each gradient can be computed using a .backward() from task to output, then added together and weightied with the corresponding task weights.
        It is not clear if it is faster this way or to directly use autograd / backward until the last shared layer and a global backward.
        """
        if self._is_training(loss):
            self.gradients = self.gtb.compute_gradients(loss).to(self.device)
        else:
            self.gradients = self.gtb.initialize_gradients().to(self.device)

    def _gradients_update(self) -> None:
        for i, k in enumerate(self.targets.keys()):
            self.gradients_dict[k] = self.gradients[i].clone().detach()

    def forward(self, loss: dict[str, torch.Tensor], module: LightningModule = None) -> dict:
        self._set_device(loss)
        self._set_layer(module)
        self._setup(loss, module)

        if self.requires_gradients:
            self._gradients_compute(loss)
            self._gradients_update()

        self._weights_compute(loss, module)
        self._weights_update()

        return self._weights_apply(loss)
