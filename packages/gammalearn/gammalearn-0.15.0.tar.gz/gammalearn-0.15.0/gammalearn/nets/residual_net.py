import logging
from typing import Tuple

import torch.nn
import torch.nn as nn

from gammalearn.nets.base import BaseBlock
from gammalearn.nets.sequential import ExtraKWArgsInForwardSequential


class ResidualLayerCartesian(BaseBlock):
    """
    Implementation of the residual block for interpolated CTAO images (cartesian grid).
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        downsample: bool = False,
        pre_activation: bool = True,
        normalization: Tuple[nn.Module, dict] = None,
        non_linearity: Tuple[nn.Module, dict] = (nn.ReLU, {}),
    ):
        super().__init__()
        self.shortcut = ExtraKWArgsInForwardSequential()
        if downsample:
            stride = 2
            self.add_normalization(self.shortcut, "_shortcut", in_features, normalization)
            self.add_activation(self.shortcut, "_shortcut", non_linearity)
            self.shortcut.add_module(
                "cv_shortcut", nn.Conv2d(in_features, out_features, kernel_size=3, stride=stride, padding=1)
            )
        else:
            stride = 1
            self.shortcut.add_module("id", nn.Identity())

        self.conv_block = ExtraKWArgsInForwardSequential()
        if pre_activation:
            self.add_normalization(self.conv_block, "1", in_features, normalization)
            self.add_activation(self.conv_block, "1", non_linearity)

        self.conv_block.add_module(
            "cv1", nn.Conv2d(in_features, out_features, kernel_size=3, stride=stride, padding=1)
        )
        self.add_normalization(self.conv_block, "2", out_features, normalization)
        self.add_activation(self.conv_block, "2", non_linearity)
        self.conv_block.add_module(
            "cv2", nn.Conv2d(out_features, out_features, kernel_size=3, padding=1)
        )  # stride=1 here

    def forward(self, x, **kwargs):
        return self.conv_block(x, **kwargs) + self.shortcut(x, **kwargs)


class ResNetAttention(BaseBlock):
    """
    ResNet like Network based on https://arxiv.org/abs/1603.05027, CIFAR version with full pre-activation,
    augmented with attention (see backbone definition :
    https://www.scitepress.org/Link.aspx?doi=10.5220/0010297405340544)

    The model is a stack of residual layers, followed by an adaptative pooling layer allowing to get the desired latent-space dimension
    """

    def __init__(self, net_parameters_dic):
        """

        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network

        """
        super().__init__()
        self.logger = logging.getLogger(__name__ + ".ResNetAttention")

        num_layers = net_parameters_dic["num_layers"]
        num_channels = [net_parameters_dic["num_channels"]]
        block_features = net_parameters_dic["block_features"]
        num_channels.extend(block_features)
        attention = net_parameters_dic.get("attention_layer", None)
        output_size = net_parameters_dic["output_size"]
        non_linearity = net_parameters_dic.get("non_linearity", (torch.nn.ReLU, {}))
        normalization = net_parameters_dic.get("normalization", None)
        initialization = net_parameters_dic.get(
            "initialization", (torch.nn.init.kaiming_uniform_, {"mode": "fan_out"})
        )
        freeze = net_parameters_dic.get("freeze", False)
        self.num_features = num_channels[-1]

        # Check normalization and activation and convert to tuple if necessary
        normalization = self.check_normalization(normalization)
        non_linearity = self.check_activation(non_linearity)

        # ResNet backbone
        self.feature = ExtraKWArgsInForwardSequential()

        # Layer 0
        self.feature.add_module("cv0", nn.Conv2d(num_channels[0], block_features[0], 3, padding=1))
        self.add_activation(self.feature, "0", non_linearity)

        # blocks
        for i, (n_in, n_out) in enumerate(zip(num_channels[:-1], num_channels[1:])):
            if i == 0:  # special case for the first layer, that has different input shape
                for n in range(1, num_layers + 1):
                    pre_activation = False if n == 1 else True

                    layer = ResidualLayerCartesian(
                        n_out,
                        n_out,
                        pre_activation=pre_activation,
                        normalization=normalization,
                        non_linearity=non_linearity,
                    )
                    self.feature.add_module("block" + str(i) + "_layer" + str(n), layer)
            else:
                for n in range(1, num_layers + 1):
                    in_features = n_in if n == 1 else n_out
                    downsample = True if n == 1 else False

                    layer = ResidualLayerCartesian(
                        in_features,
                        n_out,
                        downsample=downsample,
                        normalization=normalization,
                        non_linearity=non_linearity,
                    )
                    self.feature.add_module("block" + str(i) + "_layer" + str(n), layer)

            if attention is not None:
                self.feature.add_module("attention_block" + str(i), attention[0](n_out, **attention[1]))

        self.add_activation(self.feature, "_last", non_linearity)
        self.adaptive_pooling = nn.AdaptiveAvgPool2d(output_size)
        self.feature.add_module("adaptive_pooling2D", self.adaptive_pooling)

        # Compute the number of pixels (where idx is not -1 in the index matrix) of the last features
        self.n_pixels = torch.prod(torch.tensor(output_size))
        self.logger.info("num pixels after last pooling : {}".format(self.n_pixels))

        self.initialize_weights(self.modules(), method=initialization)
        self.freeze_weights(self.feature, freeze=freeze)

    def forward(self, x: torch.Tensor, **kwargs):
        return self.feature(x, **kwargs)
