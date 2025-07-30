import torch
import torch.nn as nn
from lightning import LightningModule

from gammalearn.criterion.loss_balancing.loss_balancing import MultiLossBalancing


class GradNorm(MultiLossBalancing):
    """
    From the article GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks (
    https://arxiv.org/abs/1711.02257). The method consists in computing the gradients of the loss with respect to the
    shared weights and then compute the norm of the gradients. The weights are then updated according to the norm of
    the gradients.
    Inspired from https://github.com/NVIDIA/modulus-sym/blob/main/modulus/sym/loss/aggregator.py#L111.
    """

    def __init__(
        self,
        targets: dict[str, dict],
        alpha: float = 1.0,
        layer: nn.Module = None,
        requires_gradients: bool = True,
    ):
        super().__init__(
            targets=targets,
            balancing=True,
            requires_gradients=requires_gradients,
            layer=layer,
        )
        assert alpha > 0, "Parameter alpha of GradNorm must be strictly positive"
        self.alpha = alpha
        self.weights = nn.Parameter(torch.zeros(len(self.targets)))  # exp(0) = 1
        self.L_grad = torch.tensor(0.0, requires_grad=True)
        self.l0 = torch.zeros(len(self.targets))

        self.tracker_g = None  # Gradient norms
        self.tracker_r = None  # Relative inverse training rate
        self.tracker_k = None  # The constant of the L_grad objective function
        self.tracker_l = None  # The relative loss
        self.tracker_l0 = None  # The initial loss
        self.tracker_lgrad = None  # The L_grad objective function

    def _setup(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        if self._is_first_iter(module) and self._is_training(loss):
            self.l0 = torch.stack([loss[k].clone().detach() for k in self.targets.keys()]).to(self.device)

    def _weights_compute(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        if self._is_training(loss):
            self._weights_normalize()
            weights_exp = self._t(self.weights)

            # Compute the norm of the gradient of each task wrt to the last shared layer
            G = torch.mul(weights_exp.view(-1, 1), self.gradients.detach()[self.gi]).norm(dim=1, p=2)

            # Compute the relative inverse training rate
            loss_copy = torch.stack([loss[k].clone().detach() for k in self.targets.keys()]).to(self.device)
            loss_ratio = torch.div(loss_copy, self.l0)[self.gi]
            r = torch.div(loss_ratio, loss_ratio.mean())

            # Compute the gradient gradients
            constant = torch.mul(G.mean(), torch.pow(r, self.alpha)).detach()
            L_grad = torch.sub(G, constant).norm(p=1)
            self.L_grad = L_grad

            # Track the values
            self.tracker_g = {k: G[i].detach() for i, k in enumerate(self.targets.keys())}
            self.tracker_r = {k: r[i].detach() for i, k in enumerate(self.targets.keys())}
            self.tracker_k = {k: constant[i].detach() for i, k in enumerate(self.targets.keys())}
            self.tracker_l = {k: loss_ratio[i].detach() for i, k in enumerate(self.targets.keys())}
            self.tracker_l0 = {k: self.l0[i].detach() for i, k in enumerate(self.targets.keys())}
            self.tracker_lgrad = L_grad.detach()

    def _t(self, weight: torch.Tensor) -> torch.Tensor:
        """
        Exponantial transformation of the weights using w_i = exp(w_i) to ensure the weights are positive.
        """
        return torch.exp(weight)

    def _weights_normalize(self) -> None:
        """
        Normalize the weights using c*exp(x) = exp(log(c)+x).
        """
        with torch.no_grad():
            c = torch.div(len(self.targets), self._t(self.weights).sum())
            for i in range(len(self.targets)):
                self.weights[i] = self.weights[i].clone() + torch.log(c).detach()

    def _weights_apply(self, loss: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = self._t(self.weights[i]) * loss[k]

        weighted_loss["gradnorm"] = self.L_grad

        return weighted_loss
