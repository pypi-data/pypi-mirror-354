import importlib
from pathlib import Path

import torch
import torch.nn as nn

from gammalearn.experiment_runner import Experiment
from gammalearn.gammalearn_lightning_module import LitGLearnModule
from gammalearn.nets.auto_encoder import Encoder, LinearBlock
from gammalearn.nets.domain_adaptation import DANN
from gammalearn.nets.residual_net import ResNetAttention


class ADistance(nn.Module):
    """
    Calculate the A-distance between two distributions. The A-distance is a measure of discrepancy that can be computed
    with a domain classifier.
    Inspired from https://github.com/thuml/Transfer-Learning-Library/blob/master/tllib/utils/analysis/a_distance.py.
    """

    def __init__(self, net_parameters_dic: dict):
        super().__init__()
        checkpoint = net_parameters_dic.get("checkpoint", None)
        freeze_backbone = net_parameters_dic.get("freeze_backbone", False)
        output_shape = net_parameters_dic.get("output_shape", 2)

        if checkpoint is not None:
            self.load_from_checkpoint(checkpoint)
        else:
            self.load_from_model(net_parameters_dic)

        if freeze_backbone:
            self.freeze_backbone()

        if hasattr(self.feature, "n_latent_features"):  # UNet, AE, VAE
            n_latent_features = self.feature.n_latent_features
        else:  # ResNetAttention
            n_latent_features = self.feature.n_pixels * self.feature.num_features

        # Implement the non-trained classifier
        self.classifier = nn.Sequential()
        if net_parameters_dic.get("fc_features", None) is not None:
            self.classifier.add_module(
                "fc1_features", LinearBlock(n_latent_features, net_parameters_dic.get("fc_features"))
            )
            self.classifier.add_module("fc2_features", nn.Linear(net_parameters_dic.get("fc_features"), output_shape))
        else:
            self.classifier.add_module("fc1_features", nn.Linear(n_latent_features, output_shape))

    def load_experiment_settings(self, configuration_file: Path) -> Experiment:
        spec = importlib.util.spec_from_file_location("settings", configuration_file)
        settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings)
        return Experiment(settings)

    def freeze_backbone(self) -> None:
        for param in self.feature.parameters():
            param.requires_grad = False

    def load_from_model(self, net_parameters_dic: dict) -> None:
        main_task_model = net_parameters_dic["main_task"]["model"](net_parameters_dic["main_task"]["parameters"])
        if isinstance(main_task_model, DANN):
            self.feature = main_task_model.main_task_model.feature
        elif isinstance(main_task_model, (ResNetAttention, Encoder)):
            self.feature = main_task_model
        else:
            self.feature = main_task_model.feature

    def load_from_checkpoint(self, checkpoint: dict) -> None:
        try:
            experiment = self.load_experiment_settings(checkpoint["experiment"])
            checkpoint_path = checkpoint["checkpoint_path"]
            module = LitGLearnModule.load_from_checkpoint(checkpoint_path=checkpoint_path, experiment=experiment)
        except Exception as e:
            raise ValueError(e)

        # Get the pre-trained backbone
        model = module.net
        if hasattr(model, "main_task_model"):  # DANN
            self.feature = model.main_task_model.feature
        elif hasattr(model, "feature"):  # GammaPhysNet
            self.feature = model.feature
        else:  # ResNetAttention / backbone...
            self.feature = model

    def forward(self, x: torch.Tensor, **kwargs) -> dict:
        x = self.feature(x)

        if isinstance(x, (tuple, list)):  # UNet, AE, VAE
            output_class = x[-1].flatten(start_dim=1)
        else:
            output_class = x.flatten(start_dim=1)
        output_class = self.classifier(output_class)
        # output_class = self.softmax(output_class)  # CE loss doesn't need softmax

        return {"domain_class": output_class}
