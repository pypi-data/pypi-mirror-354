from typing import Any, Tuple

import torch
import torch.nn as nn
from indexedconv.engine import IndexedConv

from gammalearn.nets.conditional_batch_normalization import CBN


class BaseBlock(nn.Module):
    """Base class of the GLearn Module that allows to set the activation, initialization, normalization function of the all the backbone layers or all the multi-task layers.
    Also allows to freeze all layers in the model, to for instance freeze only the backbone and fine-tune the multitask
    """

    def __init__(self):
        super().__init__()

    def check_normalization(self, normalization: Tuple[torch.nn.Module, dict]) -> Tuple[torch.nn.Module, dict]:
        """Transform the provided normalization into a tuple (1st tuple element is the normalization function, others are the normalization functions arguments)"""
        if normalization is not None:
            if not isinstance(normalization, tuple):
                normalization = (normalization, {})
        return normalization

    def add_normalization(
        self,
        module: torch.nn.Sequential,
        layer_name: str,
        num_channels: torch.Tensor,
        normalization: Tuple[torch.nn.Module, dict],
    ) -> None:
        """
        Function to add normalization layer to a layer module.
        """
        if normalization is not None:
            if normalization[0] == torch.nn.BatchNorm1d:
                normalization[1]["num_features"] = num_channels

            elif normalization[0] == torch.nn.BatchNorm2d:
                normalization[1]["num_features"] = num_channels

            elif normalization[0] == torch.nn.LayerNorm:
                return NotImplementedError

            elif normalization[0] == torch.nn.InstanceNorm2d:
                normalization[1]["num_features"] = num_channels

            elif normalization[0] == torch.nn.GroupNorm:
                normalization[1]["num_channels"] = num_channels

            elif normalization[0] == CBN:
                normalization[1]["hidden_size"] = normalization[1].get("hidden_size", normalization[1]["input_size"])
                normalization[1]["output_size"] = num_channels

            else:
                raise ValueError("Unknown normalization")

            module.add_module(normalization[0].__name__ + layer_name, normalization[0](**normalization[1]))

    def check_activation(self, activation: Tuple[torch.nn.Module, dict]) -> Tuple[torch.nn.Module, dict]:
        """Transform the provided activation into a tuple (1st tuple element is the activation function, others are the activation functions arguments)"""
        if activation is not None:
            if not isinstance(activation, tuple):
                activation = (activation, {})
        return activation

    def add_activation(
        self, module: torch.nn.Sequential, layer_name: str, activation: Tuple[torch.nn.Module, dict]
    ) -> None:
        """
        Function to add activation layer to a module layer.
        """
        if activation is not None:
            module.add_module(activation[0].__name__ + layer_name, activation[0](**activation[1]))

    def check_initialization(self, initialization: Tuple[Any, dict]) -> Tuple[Any, dict]:
        """Transform the provided initialization into a tuple (1st tuple element is the initialization function, others are the initialization functions arguments)"""
        if initialization is not None:
            if not isinstance(initialization, tuple):
                initialization = (initialization, {})
        return initialization

    def initialize_weights(
        self, modules: torch.nn.Module, method: Any = (torch.nn.init.kaiming_uniform_, {"mode": "fan_out"})
    ) -> None:
        """Initialize all the convolution and linear layers in the module"""
        for m in modules:
            if isinstance(m, (nn.Conv2d, IndexedConv, nn.Linear)):
                method[0](m.weight, **method[1])

    def freeze_weights(self, weights: torch.nn.Module, freeze: bool = False):
        """Freeze all weights in the model"""
        if freeze:
            for w in weights.parameters():
                w.requires_grad = False
