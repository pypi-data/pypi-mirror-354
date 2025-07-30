import logging

import torch
import torch.nn as nn

from gammalearn.nets.base import BaseBlock


class LinearBlock(BaseBlock):
    """Fully connected encoder block layer to encode the conditional input of the CBN layer"""

    def __init__(self, input_size: int, output_size: int, normalization=None, non_linearity=None, name: str = ""):
        super().__init__()
        self.linear_block = nn.Sequential()
        self.linear_block.add_module("linear0", nn.Linear(input_size, output_size))
        if normalization is not None:
            self.add_normalization(self.linear_block, name, output_size, normalization)
        if non_linearity is not None:
            self.add_activation(self.linear_block, name, non_linearity)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_block(x)


class LinearEncoder(BaseBlock):
    """
    Encoder for the conditional batch normalization. Applicable for 1-D inputs.
    """

    def __init__(self, net_parameters_dic) -> None:
        super().__init__()
        num_layers = net_parameters_dic["num_layers"]
        input_size = net_parameters_dic["input_size"]
        hidden_size = net_parameters_dic["hidden_size"]
        output_size = net_parameters_dic["output_size"]
        initialization = net_parameters_dic.get(
            "initialization", (torch.nn.init.kaiming_uniform_, {"mode": "fan_out"})
        )
        non_linearity = net_parameters_dic.get("non_linearity", (torch.nn.ReLU, {}))
        normalization = net_parameters_dic.get("normalization", None)

        # Check normalization and activation and convert to tuple if necessary
        normalization = self.check_normalization(normalization)
        non_linearity = self.check_activation(non_linearity)

        if isinstance(hidden_size, int):
            hidden_size = [hidden_size] * num_layers

        # Create encoder
        self.encoder = nn.Sequential()
        self.encoder.add_module(
            "linear_block0", LinearBlock(input_size, hidden_size[0], normalization, non_linearity, "0")
        )
        for i in range(1, num_layers):
            self.encoder.add_module(
                "linear_block" + str(i),
                LinearBlock(hidden_size[i - 1], hidden_size[i], normalization, non_linearity, str(i)),
            )
        self.encoder.add_module(
            "linear_block" + str(num_layers), LinearBlock(hidden_size[-1], output_size, None, None, str(num_layers))
        )

        self.initialize_weights(self.modules(), method=initialization)

    def forward(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        return self.encoder(x)


class ConvBlock(BaseBlock):
    """
    Basic convolutional block, inspired from https://github.com/milesial/Pytorch-UNet.
    The padding is set to '1' so the fixed kernel size of '3' has no edge effects.
    """

    def __init__(
        self, in_channels, out_channels, normalization=(nn.BatchNorm2d, {}), non_linearity=(torch.nn.ReLU, {})
    ):
        super().__init__()

        # Check normalization and activation and convert to tuple if necessary
        normalization = self.check_normalization(normalization)
        non_linearity = self.check_activation(non_linearity)

        self.conv_block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv_block(x)


class ConvBlockDown(nn.Module):
    """
    Basic convolution block for an encoder, inspired from https://github.com/milesial/Pytorch-UNet.
    """

    def __init__(self, in_channels, out_channels, latent_feature_size=None):
        super().__init__()

        if latent_feature_size is None:
            self.conv_block_down = nn.Sequential(
                nn.MaxPool2d(2),
                ConvBlock(in_channels, out_channels),
            )
        else:
            # Usually used as the last layer of the encoder
            self.conv_block_down = nn.Sequential(
                nn.AdaptiveAvgPool2d(latent_feature_size),
                ConvBlock(in_channels, out_channels),
            )

    def forward(self, x):
        return self.conv_block_down(x)


class ConvBlockUp(nn.Module):
    """
    Basic convolution block for a decoder, inspired from https://github.com/milesial/Pytorch-UNet.
    """

    def __init__(self, in_channels, out_channels, unet=False):
        super().__init__()
        self.unet = unet  # Allow connections between decoder and encoder
        mid_channels = in_channels + out_channels if self.unet else in_channels
        self.conv_block_up = nn.ConvTranspose2d(in_channels, in_channels, kernel_size=2, stride=2)
        self.conv_block = ConvBlock(mid_channels, out_channels)

    def forward(self, x1, x2):
        x2 = self.conv_block_up(x2)

        diff_y = x1.size()[2] - x2.size()[2]
        diff_x = x1.size()[3] - x2.size()[3]

        x2 = torch.nn.functional.pad(x2, [diff_x // 2, diff_x - diff_x // 2, diff_y // 2, diff_y - diff_y // 2])

        x = torch.cat([x2, x1], dim=1) if self.unet else x2

        return self.conv_block(x)


class Encoder(nn.Module):
    """
    Encoder module used by auto-encoder: UNet or VAE.
    """

    def __init__(self, net_parameters_dic):
        super().__init__()
        n_channels = net_parameters_dic["n_channels"]  # Number of input channels
        latent_feature_size = net_parameters_dic["latent_feature_size"]  # The expected shape of the latent space
        block_features = [n_channels] + net_parameters_dic["block_features"]

        # To make auto-encoder, UNet or VAE compatible with DANN, the following arguments must be set.
        self.num_features = block_features[-1]
        self.n_pixels = torch.prod(torch.tensor(latent_feature_size))
        self.n_latent_features = self.n_pixels * self.num_features  # The number of coordinates in the latent space

        # Definition of the encoder. The first layer is a classic convolution block, and the last layer receives the
        # expected latent space shape defined in the network parameters dictionary.
        encoder = [ConvBlock(n_channels, block_features[1])]
        for i in range(2, len(block_features) - 1):
            encoder.append(ConvBlockDown(block_features[i - 1], block_features[i]))
        encoder.append(ConvBlockDown(block_features[-2], block_features[-1], latent_feature_size=latent_feature_size))
        self.encoder = nn.Sequential(*encoder)

    def forward(self, x, sequence=True):
        output = []
        for i, module in enumerate(self.encoder):
            output.append(module(x))
            x = output[i]

        return output if sequence else output[-1]


class Decoder(nn.Module):
    """
    Decoder module for auto-encoder, UNet or VAE.
    """

    def __init__(self, net_parameters_dic, unet=False):
        super().__init__()
        n_channels = net_parameters_dic["n_channels"]  # Number of input channels
        block_features = net_parameters_dic["block_features"][::-1] + [n_channels]

        # Definition of the decoder. The last layer receives the number of expected output channels defined in the
        # network parameters dictionary.
        decoder = []
        for i in range(1, len(block_features) - 1):
            decoder.append(ConvBlockUp(block_features[i - 1], block_features[i], unet=unet))
        decoder.append(ConvBlock(block_features[-2], n_channels))
        self.decoder = nn.Sequential(*decoder)

    def forward(self, x, sequence=True):
        x = x[::-1]
        output = []
        tmp = x[0]
        for i, module in enumerate(self.decoder[:-1]):
            output.append(module(x[i + 1], tmp))
            tmp = output[-1]
        output.append(self.decoder[-1](tmp))

        return output if sequence else output[-1]


class AutoEncoder(nn.Module):
    """Auto-encoder (back-bone + decoder) used for the digits experiments"""

    def __init__(self, net_parameters_dic):
        super().__init__()
        self.logger = logging.getLogger(__name__ + ".AutoEncoder")
        self.encoder = Encoder(net_parameters_dic)
        self.decoder = Decoder(net_parameters_dic)

    def forward(self, x: torch.Tensor, **kwargs):
        x = self.decoder(self.encoder(x))

        return {"autoencoder": x[-1]}


class UNet(nn.Module):
    """Auto-encoder (back-bone + decoder) used for the digits experiments"""

    def __init__(self, net_parameters_dic):
        super().__init__()
        self.logger = logging.getLogger(__name__ + ".UNet")
        self.encoder = Encoder(net_parameters_dic)
        self.decoder = Decoder(net_parameters_dic, unet=True)

    def forward(self, x: torch.Tensor, **kwargs):
        x = self.decoder(self.encoder(x))

        return {"autoencoder": x[-1]}
