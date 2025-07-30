import re

import torch
import torch.optim as optim


def load_sgd(net, parameters):
    """
    Load the SGD optimizer
    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    assert "lr" in parameters.keys(), "Missing learning rate for the optimizer !"
    assert "weight_decay" in parameters.keys(), "Missing weight decay for the optimizer !"
    return optim.SGD(net.parameters(), **parameters)


def load_adam(net, parameters):
    """
    Load the Adam optimizer
    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    assert "lr" in parameters.keys(), "Missing learning rate for the optimizer !"

    return optim.Adam(net.parameters(), **parameters)


def load_adam_w(net, parameters):
    """
    Load the Adam optimizer
    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    assert "lr" in parameters.keys(), "Missing learning rate for the optimizer !"

    return optim.AdamW(net.parameters(), **parameters)


def load_rmsprop(net, parameters):
    """
    Load the RMSprop optimizer
    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    assert "lr" in parameters.keys(), "Missing learning rate for the optimizer !"

    return optim.RMSprop(net.parameters(), **parameters)


def load_per_layer_sgd(net, parameters):
    """
    Load the SGD optimizer with a different learning rate for each layer.

    This is SGD, but with a learning rate that decreases the nearest in the net the layer is from the input
    the closer to the input the layer is, the lower the learning rate

    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    assert "lr" in parameters.keys(), "Missing learning rate for the optimizer !"
    assert "weight_decay" in parameters.keys(), "Missing weight decay for the optimizer !"
    assert "alpha" in parameters.keys(), "Missing alpha !"

    lr_default = parameters["lr"]
    alpha = parameters.pop("alpha")

    feature_modules = []  # The feature parameters
    base_modules = []  # The other parameters
    for name, module in net.named_modules():
        if isinstance(module, torch.nn.Linear) or isinstance(module, torch.nn.Conv2d):
            if name.split(".")[0] == "feature":
                feature_modules.append(module)
            else:
                base_modules.append(module)

    feature_lr = [lr_default / (alpha**layer) for layer in range(1, len(feature_modules) + 1)]
    feature_lr.reverse()

    parameter_group = [{"params": p.parameters()} for p in base_modules]
    parameter_group += [{"params": p.parameters(), "lr": lr} for p, lr in zip(feature_modules, feature_lr)]

    return torch.optim.SGD(parameter_group, **parameters)


def prime_optimizer(net: torch.nn.Module, parameters: dict) -> torch.optim.Optimizer:
    """
    Load the optimizer for Masked AutoEncoder fine tuning (transformers)

    Like the SGD per layer optimizer, but for the transformer models.
    Used for fine-tuning the transformers, in the supervised training after the unsupervised encoding-decoding training


    Parameters
    ----------
    net (nn.Module): the network of the experiment
    parameters (dict): a dictionary describing the parameters of the optimizer

    Returns
    -------
    the optimizer
    """
    num_blocks = len(list(net.encoder.children())) + 1
    layer_scales = [parameters["layer_decay"] ** (num_blocks - i) for i in range(num_blocks + 1)]

    no_weight_decay = ["pos_embedding", "additional_tokens"]

    param_groups = {}

    for n, p in net.named_parameters():
        if p.requires_grad:
            # Non weight decay
            if p.ndim == 1 or n in no_weight_decay:
                this_decay = 0.0
            else:
                this_decay = None

            layer_id = get_layer_id_for_prime(n)
            group_name = str(layer_id) + "_" + str(this_decay)
            if group_name not in param_groups:
                layer_scale = layer_scales[layer_id]
                param_groups[group_name] = {
                    # 'lr_scale': layer_scale,
                    "lr": layer_scale * parameters["optimizer_parameters"]["lr"],
                    "params": [],
                }
                if this_decay is not None:
                    param_groups[group_name]["weight_decay"] = this_decay
            param_groups[group_name]["params"].append(p)
    return parameters["optimizer"](list(param_groups.values()), **parameters["optimizer_parameters"])


def get_layer_id_for_prime(name: str) -> int:
    """
    Retrieve GammaPhysNetPrime layer id from parameter name
    """
    if any(layer in name for layer in ["pos_embedding", "patch_projection"]):
        return 0
    else:
        try:
            block = re.findall(r"enc_block_\d", name)[0]
            block = int(block.split("_")[-1]) + 1
            return block
        except IndexError:
            return -1
