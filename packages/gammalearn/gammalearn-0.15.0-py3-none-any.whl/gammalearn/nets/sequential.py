import torch
import torch.nn as nn

from gammalearn.nets.base import BaseBlock
from gammalearn.nets.conditional_batch_normalization import CBN


class ExtraKWArgsInForwardSequential(nn.Sequential):
    """
    Sequential module with conditioned batch normalization.

    This is required to pass some more arguments to the forward of the modules
    """

    def __init__(self, *args):
        super().__init__(*args)

    def forward(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        for module in self:
            if isinstance(module, (BaseBlock, CBN)):
                x = module(x, **kwargs)
            else:
                x = module(x)
        return x
