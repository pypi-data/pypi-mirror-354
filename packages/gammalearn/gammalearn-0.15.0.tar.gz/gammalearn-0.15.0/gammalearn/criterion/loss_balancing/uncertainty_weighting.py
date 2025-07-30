import torch
import torch.nn as nn
from lightning import LightningModule

from gammalearn.criterion.loss_balancing.loss_balancing import MultiLossBalancing


class UncertaintyWeighting(MultiLossBalancing):
    r"""Loss in case of multi regression experiment with homoscedastic uncertainty loss balancing.

    In [1]_ they define the loss as

    .. math:: \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{2\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2


    but in https://github.com/yaringal/multi-task-learning-example/blob/master/multi-task-learning-example.ipynb as

    .. math:: \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -1


    should not make a big difference. However, we introduce log_var_coefficients and penalty to let the user choose:

    .. math:: \text{L} = \sum_i \frac{1}{\text{log_var_coefficients}\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -\text{penalty}

    Parameters
    ----------
    targets : dict
        The loss dictionary defining for every objective of the experiment the loss function and its initial log_var

    References
    ----------
    .. [1] Alex Kendall and Yarin Gal and Roberto Cipolla, "Multi-Task Learning Using Uncertainty to Weigh Losses for Scene
        Geometry and Semantics" CoRR, abs/1705.07115, 2017, http://arxiv.org/abs/1705.07115
    """

    def __init__(
        self,
        targets: dict[str, dict],
        log_var_coefficients: list = None,
        penalty: int = 0,
        requires_gradients: bool = False,
        layer: str = None,
    ):
        super().__init__(
            targets=targets,
            balancing=True,
            requires_gradients=requires_gradients,
            layer=layer,
        )
        self.weights = torch.Tensor(torch.ones(len(self.targets)))
        self.log_vars = nn.Parameter(torch.ones(len(self.targets)), requires_grad=True)
        self.penalty = penalty

        if log_var_coefficients is None:
            # If the log var coefficients have not been initialized in the experiment setting file, initialize them to 1
            self.log_var_coefficients = torch.ones(self.log_vars.shape)
        else:
            self.log_var_coefficients = torch.tensor(log_var_coefficients)
        assert len(self.log_vars) == len(
            self.log_var_coefficients
        ), "The number of log variance coefficients must be equal to the number of log variances."

    def _weights_compute(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        for i in range(len(self.targets)):
            self.weights[i] = (torch.exp(-self.log_vars[i]) * self.log_var_coefficients[i]).to(self.device)

    def _weights_apply(self, loss: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = (
                (torch.exp(-self.log_vars[i]) * self.log_var_coefficients[i]) * loss[k]
                + self.log_vars[i]
                - self.penalty
            )

        return weighted_loss
