import logging

import torch
import torch.nn as nn

from gammalearn.nets.base import BaseBlock


class GammaPhysNet(BaseBlock):
    """
    Gamma-PhysNet with ResNet (back-bone + multi-task)
    Please cite and see details: https://www.scitepress.org/Link.aspx?doi=10.5220/0010297405340544
    """

    def __init__(self, net_parameters_dic):
        """

        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network
        """
        super(GammaPhysNet, self).__init__()
        self.logger = logging.getLogger(__name__ + ".GammaPhysNet")

        fc_width = net_parameters_dic.get("fc_width", 100)
        non_linearity = net_parameters_dic.get("non_linearity", (torch.nn.ReLU, {}))
        last_bias_init = net_parameters_dic.get("last_bias_init", None)
        self.non_linearity = (
            non_linearity() if not isinstance(non_linearity, tuple) else non_linearity[0](**non_linearity[1])
        )

        num_class = net_parameters_dic["targets"]["class"] if "class" in net_parameters_dic["targets"].keys() else 0
        regressor = {t: net_parameters_dic["targets"][t] for t in net_parameters_dic["targets"].keys() if t != "class"}
        if len(regressor) == 0:
            regressor = None

        # Backbone
        self.feature = net_parameters_dic["backbone"]["model"](net_parameters_dic["backbone"]["parameters"])

        # Multitasking block
        if regressor is not None:
            if "energy" in regressor:
                self.energy = nn.Sequential()
                self.energy.add_module("en_layer1", nn.Linear(self.feature.num_features, fc_width))
                self.add_activation(self.energy, non_linearity[0].__name__ + "1", non_linearity)
                self.energy.add_module("en_out", nn.Linear(fc_width, regressor["energy"]))
                if last_bias_init is not None and "energy" in last_bias_init:
                    self.energy.en_out.bias = nn.Parameter(torch.tensor(last_bias_init["energy"]))
            else:
                self.energy = None
            if "impact" in regressor or "direction" in regressor:
                self.fusion = nn.Linear(self.feature.n_pixels * self.feature.num_features, fc_width)
                if "impact" in regressor:
                    self.impact = nn.Linear(fc_width, regressor["impact"])
                    if last_bias_init is not None and "impact" in last_bias_init:
                        self.impact.bias = nn.Parameter(torch.tensor(last_bias_init["impact"]))
                else:
                    self.impact = None
                if "direction" in regressor:
                    self.direction = nn.Linear(fc_width, regressor["direction"])
                    if last_bias_init is not None and "direction" in last_bias_init:
                        self.direction.bias = nn.Parameter(torch.tensor(last_bias_init["direction"]))
                else:
                    self.direction = None
            else:
                self.fusion = None
        else:
            self.energy = None
            self.fusion = None
            self.direction = None
            self.impact = None
        if num_class > 0:
            self.classifier = nn.Linear(self.feature.n_pixels * self.feature.num_features, num_class)
            if last_bias_init is not None and "class" in last_bias_init:
                self.classifier.bias = nn.Parameter(torch.tensor(last_bias_init["class"]))
        else:
            self.classifier = None

    def forward(self, x: torch.Tensor, **kwargs):
        out = self.feature(x, **kwargs)
        out = torch.flatten(out, start_dim=2)
        out_e = torch.mean(out, 2)  # Global average pooling
        out = out.view(out.size(0), -1)
        out_tot = {}
        if self.energy is not None:
            out_tot["energy"] = self.energy(out_e)
        if self.fusion is not None:
            out_f = self.non_linearity(self.fusion(out))
            if self.impact is not None:
                out_tot["impact"] = self.impact(out_f)
            if self.direction is not None:
                out_tot["direction"] = self.direction(out_f)
        if self.classifier is not None:
            out_tot["class"] = self.classifier(out)
        return out_tot


class ConditionalGammaPhysNet(BaseBlock):
    """Builds on top the GammaPhysNet to add the fully-connected encoder for the conditioning variable input to the CBN layers"""

    def __init__(self, net_parameters_dic):
        """

        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network
        """
        super().__init__()
        self.logger = logging.getLogger(__name__ + ".ConditionalGammaPhysNet")

        # instantiate the back-bone and multi-task part
        main_task_parameters = net_parameters_dic["main_task"]["parameters"]
        self.main_task_model = net_parameters_dic["main_task"]["model"](main_task_parameters)
        self.feature = self.main_task_model.feature

        # add the fully-connected encoder of the conditional batch norm
        conditional_task_parameters = net_parameters_dic["conditional_task"]["parameters"]
        self.conditional_task_model = net_parameters_dic["conditional_task"]["model"](conditional_task_parameters)
        self.input_size = conditional_task_parameters["input_size"]

    def forward(self, x: torch.Tensor, **kwargs):
        # get the CBN inputs
        # TODO: Tailored to LinearEncoder, make it more general to support more parameters (eg lambda per pixel)
        condition_input = []
        for k, v in kwargs["transform_params"].items():
            condition_input.append(v)
        condition_input = torch.cat(condition_input, dim=1)

        condition_input = condition_input.view(x.shape[0], -1).to(x.device)
        # pass the CBN input in the fully connected layer
        kwargs["conditional_input"] = self.conditional_task_model(condition_input.to(x.device), **kwargs)
        # apply the same model
        outputs = self.main_task_model(x, **kwargs)

        return outputs
