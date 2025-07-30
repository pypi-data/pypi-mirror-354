import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class SqueezeExcite(nn.Module):
    """Squeeze and excite the output of a convolution as described in the paper https://arxiv.org/abs/1709.01507

    Module to perform Attention (per channel)
    """

    def __init__(self, num_channels, ratio):
        super(SqueezeExcite, self).__init__()
        reducted_channels = int(num_channels / ratio)
        self.reduction = nn.Linear(num_channels, reducted_channels)
        self.expand = nn.Linear(reducted_channels, num_channels)

    def forward(self, x):
        out = x.mean(dim=tuple(range(x.dim())[2:]))

        out = F.relu(self.reduction(out))
        out = torch.sigmoid(self.expand(out))

        out_size = out.size() + tuple(1 for _ in range(x.dim() - 2))
        out = x * out.view(out_size)

        return out


class SpatialAttention(nn.Module):
    """
    Spatial attention layer as described in https://arxiv.org/pdf/2001.07645.pdf and implemented in
    https://github.com/sunjesse/shape-attentive-unet/blob/master/models/attention_blocks.py
    """

    def __init__(self, channels):
        super(SpatialAttention, self).__init__()
        self.down = nn.Conv1d(channels, channels // 2, kernel_size=1, bias=False)
        self.phi = nn.Conv1d(channels // 2, 1, kernel_size=1, bias=True)
        self.bn = nn.BatchNorm1d(channels // 2)

        for m in self.modules():
            if isinstance(m, nn.Conv1d):
                n = m.out_channels
                m.weight.data.normal_(0, math.sqrt(2.0 / n))
            elif isinstance(m, nn.BatchNorm1d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        out = F.relu(self.bn(self.down(x.view(x.shape[0], x.shape[1], -1))))
        out = torch.sigmoid(self.phi(out))
        return out.reshape(
            (
                x.shape[0],
                1,
            )
            + x.shape[2:]
        )


class DualAttention(nn.Module):
    """
    Dual attention layer as described in https://arxiv.org/pdf/2001.07645.pdf and implemented in
    https://github.com/sunjesse/shape-attentive-unet/blob/master/models/attention_blocks.py
    """

    def __init__(self, in_channels, ratio):
        super(DualAttention, self).__init__()
        self.se_module = SqueezeExcite(in_channels, ratio)
        self.spa_module = SpatialAttention(in_channels)

    def forward(self, x):
        se = self.se_module(x)
        spa = self.spa_module(x)
        return se * (spa + 1)
