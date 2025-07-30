import logging
from typing import Tuple

import indexedconv.utils as cvutils
import torch
import torch.nn
import torch.nn as nn
from indexedconv.engine import IndexedConv
from typing_extensions import deprecated

from gammalearn.data.telescope_geometry import get_camera_layout_from_geom
from gammalearn.nets.base import BaseBlock
from gammalearn.nets.sequential import ExtraKWArgsInForwardSequential


@deprecated("Indexed convolutions are deprecated and will be removed in a future release!")
class ResidualLayerIndexed(BaseBlock):
    """Residual layer with indexed convolution"""

    def __init__(
        self,
        in_features: int,
        out_features: int,
        index_matrix,
        downsample: bool = False,
        pre_activation: bool = True,
        kernel_type: str = "Hex",
        normalization: Tuple[nn.Module, dict] = None,
        non_linearity: Tuple[nn.Module, dict] = (nn.ReLU, {}),
    ):
        super().__init__()
        stride = 2 if downsample else 1
        self.pooled_matrix = (
            cvutils.pool_index_matrix(index_matrix, kernel_type=kernel_type) if downsample else index_matrix
        )
        indices_cv1 = cvutils.neighbours_extraction(index_matrix, stride=stride)
        indices_cv2 = cvutils.neighbours_extraction(self.pooled_matrix)

        self.shortcut = ExtraKWArgsInForwardSequential()
        if downsample:
            self.add_normalization(self.shortcut, "_shortcut", in_features, normalization)
            self.add_activation(self.shortcut, "_shortcut", non_linearity)
            self.shortcut.add_module("cv_shortcut", IndexedConv(in_features, out_features, indices_cv1))
        else:
            self.shortcut.add_module("id", nn.Identity())

        self.conv_block = ExtraKWArgsInForwardSequential()
        if pre_activation:
            self.add_normalization(self.conv_block, "1", in_features, normalization)
            self.add_activation(self.conv_block, "1", non_linearity)

        self.conv_block.add_module("cv1", IndexedConv(in_features, out_features, indices_cv1))
        self.add_normalization(self.conv_block, "2", out_features, normalization)
        self.add_activation(self.conv_block, "2", non_linearity)
        self.conv_block.add_module("cv2", IndexedConv(out_features, out_features, indices_cv2))

    def forward(self, x, **kwargs):
        return self.conv_block(x, **kwargs) + self.shortcut(x, **kwargs)


@deprecated("Indexed convolutions are deprecated and will be removed in a future release!")
class ResNetAttentionIndexed(BaseBlock):
    """
    ResNet like Network based on https://arxiv.org/abs/1603.05027, CIFAR version with full pre-activation,
    augmented with attention (see backbone definition :
    https://www.scitepress.org/Link.aspx?doi=10.5220/0010297405340544) and implemented with indexedconv.

    similar toResNetAttention but with indexed convolution
    """

    def __init__(self, net_parameters_dic):
        """
        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network
        """
        super().__init__()
        self.logger = logging.getLogger(__name__ + ".ResNetAttentionIndexed")

        index_matrix0, camera_layout = get_camera_layout_from_geom(net_parameters_dic["camera_geometry"])

        num_layers = net_parameters_dic["num_layers"]
        num_channels = [net_parameters_dic["num_channels"]]
        block_features = net_parameters_dic["block_features"]
        num_channels.extend(block_features)
        attention = net_parameters_dic["attention_layer"]
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
        indices_conv0 = cvutils.neighbours_extraction(index_matrix0, kernel_type=camera_layout)
        self.feature.add_module("cv0", IndexedConv(num_channels[0], block_features[0], indices_conv0))
        self.add_activation(self.feature, "0", non_linearity)
        # Rearrange index matrix
        index_matrix1 = cvutils.pool_index_matrix(index_matrix0, stride=1, kernel_type=camera_layout)

        # blocks
        for i, (n_in, n_out) in enumerate(zip(num_channels[:-1], num_channels[1:])):
            if i == 0:  # special case for 1st layer that has different input shape
                for n in range(1, num_layers + 1):
                    pre_activation = False if n == 1 else True

                    layer = ResidualLayerIndexed(
                        n_out,
                        n_out,
                        index_matrix1,
                        pre_activation=pre_activation,
                        normalization=normalization,
                        non_linearity=non_linearity,
                    )
                    self.feature.add_module("block" + str(i) + "_layer" + str(n), layer)
            else:
                for n in range(1, num_layers + 1):
                    in_features = n_in if n == 1 else n_out
                    downsample = True if n == 1 else False

                    layer = ResidualLayerIndexed(
                        in_features,
                        n_out,
                        index_matrix1,
                        downsample=downsample,
                        normalization=normalization,
                        non_linearity=non_linearity,
                    )
                    if n == 1:
                        index_matrix1 = layer.pooled_matrix
                    self.feature.add_module("block" + str(i) + "_layer" + str(n), layer)
            if attention is not None:
                self.feature.add_module("attention_block" + str(i), attention[0](n_out, **attention[1]))

        self.add_activation(self.feature, "_last", non_linearity)

        # Compute the number of pixels (where idx is not -1 in the index matrix) of the last features
        self.n_pixels = int(torch.sum(torch.ge(index_matrix1[0, 0], 0)).data)
        self.logger.debug("num pixels after last pooling : {}".format(self.n_pixels))

        self.initialize_weights(self.modules(), method=initialization)
        self.freeze_weights(self.feature, freeze=freeze)

    def forward(self, x: torch.Tensor, **kwargs):
        return self.feature(x, **kwargs)
