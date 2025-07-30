import torch
from lightning import LightningModule

from gammalearn.criterion.loss_balancing.loss_balancing import MultiLossBalancing


class ManualWeighting(MultiLossBalancing):
    """
    Manual weighting of the loss. These hyperparameters must be defined in the targets dictionary of the experiment setting file.
    This class allows to compute gradients on the weights in the manual weighting scenario and can be used by the user.
    """

    def __init__(
        self,
        targets: dict[str, dict],
        requires_gradients: bool = False,
        layer: str = None,
    ) -> None:
        super().__init__(
            targets=targets,
            balancing=True,
            requires_gradients=requires_gradients,
            layer=layer,
        )
        self.weights = torch.Tensor([1.0] * len(self.targets))  # Equal 1. by default

    def _weights_compute(self, loss: dict[str, torch.Tensor], module: LightningModule) -> None:
        self.weights = self._weights_fetch(module)
