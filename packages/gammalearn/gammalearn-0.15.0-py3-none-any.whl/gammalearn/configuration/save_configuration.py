import collections
import json
import os
from importlib.metadata import version as runtime_version

from gammalearn.criterion.loss_balancing.loss_weight_scheduler import BaseW
from gammalearn.data.base_data_module import fetch_data_module_settings


def format_name(name):
    name = format(name)
    name = name.replace("<", "").replace(">", "").replace("class ", "").replace("'", "").replace("function ", "")
    return name.split(" at ")[0]


def dump_config_filters(exp_settings, experiment, train, domain):
    """Format the experiment settings filters"""
    data_module = fetch_data_module_settings(experiment, train=train, domain=domain)
    domain = "" if domain is None else domain

    # If test context, store the test folder path.
    if train is False:
        if data_module["paths"]:
            exp_settings["test_folders"] = data_module["paths"]

    exp_settings["files_folders " + domain] = data_module["paths"]
    if data_module["image_filter"]:
        image_filter = data_module["image_filter"]
        exp_settings["image filters " + domain] = {
            format_name(filter_func): filter_param for filter_func, filter_param in image_filter.items()
        }
    if data_module["event_filter"]:
        event_filter = data_module["event_filter"]
        exp_settings["event filters " + domain] = {
            format_name(filter_func): filter_param for filter_func, filter_param in event_filter.items()
        }

    return exp_settings


def dump_experiment_config(experiment):
    """
    Write experiment info from the settings

    Parameters
    ----------
    experiment (Experiment): experiment

    Returns
    -------

    """
    exp_settings = collections.OrderedDict(
        {
            "exp_name": experiment.experiment_name,
            "gammalearn": runtime_version("gammalearn"),
            "dataset_class": format_name(experiment.dataset_class),
            "dataset_parameters": experiment.dataset_parameters,
        }
    )
    exp_settings["network"] = {
        format_name(experiment.net_parameters_dic["model"]): {
            k: format_name(v) for k, v in experiment.net_parameters_dic["parameters"].items()
        }
    }
    if experiment.checkpoint_path is not None:
        exp_settings["resume_checkpoint"] = os.path.join(
            os.path.dirname(experiment.checkpoint_path).split("/")[-1], os.path.basename(experiment.checkpoint_path)
        )
    if experiment.info is not None:
        exp_settings["info"] = experiment.info

    if experiment.train:
        exp_settings["num_epochs"] = experiment.max_epochs
        exp_settings["batch_size"] = experiment.batch_size

        if experiment.context["train"] == "domain_adaptation":
            for domain in ["source", "target"]:
                exp_settings = dump_config_filters(exp_settings, experiment, train=True, domain=domain)
        else:
            exp_settings = dump_config_filters(exp_settings, experiment, train=True, domain=None)

        for k, v in experiment.targets.items():
            loss = format_name(v.get("loss", None))
            weight = v.get("loss_weight", None)
            if weight is not None:
                weight = None if isinstance(weight, BaseW) else weight

            exp_settings["losses"] = {k: {"loss": loss, "weight": weight}}

        exp_settings["loss_function"] = format_name(experiment.loss_balancing)
        exp_settings["optimizer"] = {key: format_name(value) for key, value in experiment.optimizer_dic.items()}
        exp_settings["optimizer_parameters"] = {
            opt: {key: format_name(value) for key, value in param.items()}
            for opt, param in experiment.optimizer_parameters.items()
        }
        if experiment.lr_schedulers is not None:
            exp_settings["lr_schedulers"] = {
                net_param: {format_name(scheduler): param for scheduler, param in scheduler_param.items()}
                for net_param, scheduler_param in experiment.lr_schedulers.items()
            }

    if experiment.test:
        if experiment.data_module_test is not None:
            exp_settings = dump_config_filters(exp_settings, experiment, train=False, domain=None)

    experiment_path = experiment.main_directory + "/" + experiment.experiment_name + "/"
    settings_path = experiment_path + experiment.experiment_name + "_settings.json"
    with open(settings_path, "w") as f:
        json.dump(exp_settings, f)
