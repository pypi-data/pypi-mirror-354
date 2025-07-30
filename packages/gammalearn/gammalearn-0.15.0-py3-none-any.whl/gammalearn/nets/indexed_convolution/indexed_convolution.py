import indexedconv.utils as cvutils
import torch.nn as nn
import torch.nn.functional as F
from indexedconv.engine import IndexedAveragePool2d, IndexedConv
from typing_extensions import deprecated


@deprecated("Indexed convolutions are deprecated and will be removed in a future release!")
class _IndexedConvLayer(nn.Sequential):
    """Indexed Convolution layer to perform 2D convolution on 1D representation"""

    def __init__(
        self,
        layer_id,
        index_matrix,
        num_input,
        num_output,
        non_linearity=nn.ReLU,
        pooling=IndexedAveragePool2d,
        pooling_kernel="Hex",
        pooling_radius=1,
        pooling_stride=2,
        pooling_dilation=1,
        pooling_retina=False,
        batchnorm=True,
        drop_rate=0,
        bias=True,
        kernel_type="Hex",
        radius=1,
        stride=1,
        dilation=1,
        retina=False,
    ):
        super(_IndexedConvLayer, self).__init__()
        self.drop_rate = drop_rate
        indices = cvutils.neighbours_extraction(index_matrix, kernel_type, radius, stride, dilation, retina)
        self.index_matrix = cvutils.pool_index_matrix(index_matrix, kernel_type=pooling_kernel, stride=1)
        self.add_module("cv" + layer_id, IndexedConv(num_input, num_output, indices, bias))
        if pooling is not None:
            p_indices = cvutils.neighbours_extraction(
                self.index_matrix, pooling_kernel, pooling_radius, pooling_stride, pooling_dilation, pooling_retina
            )
            self.index_matrix = cvutils.pool_index_matrix(
                self.index_matrix, kernel_type=pooling_kernel, stride=pooling_stride
            )
            self.add_module("pool" + layer_id, pooling(p_indices))
        if batchnorm:
            self.add_module("bn" + layer_id, nn.BatchNorm1d(num_output))
        if non_linearity is not None:
            self.add_module(non_linearity.__name__ + layer_id, non_linearity())

    def forward(self, x):
        new_features = super(_IndexedConvLayer, self).forward(x)
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        return new_features
