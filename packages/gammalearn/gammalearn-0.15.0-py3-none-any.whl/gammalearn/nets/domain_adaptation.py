import logging
from typing import Dict, Tuple

import torch
import torch.nn as nn

from gammalearn.nets.auto_encoder import LinearBlock


class GradientLayer(torch.autograd.Function):
    """
    Use to perform min-max adversarial training by reversing the gradient for the domain Adaptation.
    The goal is to inverse (and scale) the gradient coming from the domain classifier to train the encoder when using DANN.
    For DeepCoral and DeepJDot, it is only used to scale the gradient (reverse=False).
    Gradient layer. During the forward pass, the gradient remains unchanged, but is multiplied by a constant lambda_p
    during the backward pass. The context (ctx) is used to store the lambda_p variable, but can also be used to store
    any constant K. If reverse is set to True, the gradient is reversed during the backward pass.
    """

    @staticmethod
    def forward(ctx, x: torch.Tensor, K: float = 1.0, reverse: bool = False) -> torch.Tensor:
        ctx.K = K
        ctx.reverse = reverse
        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None]:
        if ctx.reverse:
            return grad_output.neg() * ctx.K, None, None
        else:
            return grad_output * ctx.K, None, None


class BaseDomainAdaptationNet(nn.Module):
    """
    Base class to implements the usage of the gradient layer to reverse/scale the gradient
    of the domain adaptation task if necessary.
    """

    def __init__(self, net_parameters_dic):
        super().__init__()
        self.logger = logging.getLogger(__name__ + "._BaseDomainNet")
        self.task = None

        # Implement the main task model
        main_task_parameters = net_parameters_dic["main_task"]["parameters"]
        self.main_task_model = net_parameters_dic["main_task"]["model"](main_task_parameters)
        self.n_latent_features = self.main_task_model.feature.n_pixels * self.main_task_model.feature.num_features

        # Hooks allow to capture the data during a forward pass. In this context, it allows us to get the backbone
        # output
        self.features = None

        def get_features_hook(module, input, output):
            self.features = output

        self.main_task_model.feature.register_forward_hook(get_features_hook)

    def get_features(self) -> torch.Tensor:
        # The UNet encoder (for example) outputs a list, of which the last element is always the feature output
        features = self.features[-1] if isinstance(self.features, (tuple, list)) else self.features

        # Reshape the latent representation from (batch_size, num_channels, (output_size))
        # to (batch_size, n_latent_features)
        return features.flatten(start_dim=1)

    def forward(self, x: torch.Tensor, **kwargs) -> Dict[str, torch.Tensor]:
        K = kwargs.get("grad_weight", 1.0)
        outputs = self.main_task_model(x, **kwargs)
        features = self.get_features()
        outputs[self.task] = GradientLayer.apply(features, K, False)

        return outputs


class DANN(BaseDomainAdaptationNet):
    """
    Domain Adversarial Neural Network (DANN) based on the following article https://arxiv.org/abs/1505.07818.
    This entity consists of the addition of a domain classifier in parallel of the classification and regression tasks.
    Experimentally, convergence is observed only if the domain classifier contains at least 2 fully-connected layers.
    """

    def __init__(self, net_parameters_dic):
        super().__init__(net_parameters_dic)
        self.logger = logging.getLogger(__name__ + ".DANN")
        self.task = "domain_class"

        # Implement the domain classifier
        fc_features = net_parameters_dic.get("fc_features", 100)
        non_linearity = net_parameters_dic.get("non_linearity", (torch.nn.ReLU, {}))
        normalization = net_parameters_dic.get("normalization", None)

        self.domain_classifier = nn.Sequential()
        self.domain_classifier.add_module(
            "fc1_domain", LinearBlock(self.n_latent_features, fc_features, normalization, non_linearity)
        )
        self.domain_classifier.add_module("fc2_domain", nn.Linear(fc_features, 2))

    def forward(self, x, **kwargs):
        K = kwargs.get("grad_weight", 1.0)
        outputs = self.main_task_model(x, **kwargs)
        features = self.get_features()
        outputs[self.task] = self.domain_classifier(GradientLayer.apply(features, K, True))

        return outputs
