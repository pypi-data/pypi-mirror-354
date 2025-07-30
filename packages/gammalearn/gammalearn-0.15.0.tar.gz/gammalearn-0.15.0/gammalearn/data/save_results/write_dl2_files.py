import os
from importlib.metadata import version as runtime_version

import numpy as np
import pandas as pd
import tables
import torch
from ctapipe.io import HDF5TableWriter
from lightning import Callback
from lstchain.io import write_dl2_dataframe
from lstchain.io.io import dl1_params_lstcam_key, write_dataframe
from lstchain.reco.utils import add_delta_t_key
from tables.scripts.ptrepack import copy_leaf
from torch.utils.data import Subset

import gammalearn.configuration.constants as csts
from gammalearn.configuration.constants import GAMMA_ID
from gammalearn.data.LST_dataset import BaseLSTDataset

def prepare_dict_of_tensors(dic):
    """
    Prepare a dictionary of tensors for serialization.

    This function takes a dictionary where values are PyTorch tensors,
    and processes each tensor to ensure it is suitable for conversion
    to a list format, typically for saving to a file. The function removes
    extra dimensions from the tensors and converts them to lists.

    Parameters
    ----------
    dic : dict
        A dictionary where keys are strings and values are PyTorch tensors.

    Returns
    -------
    dict
        A new dictionary with the same keys as the input, but with tensor
        values converted to lists.  If the tensor has more than one dimension,
        it is reshaped to a 2D tensor before conversion. If the tensor has only
        one dimension, it is directly converted to a list.  If the tensor has
        zero dimension, it is converted to a primitive python type.

    Notes
    -----
    - The function modifies the tensors in-place using squeeze_().
    - The function assumes that the tensors have at most 3 dimensions.
    """
    new_dic = {}
    for k, v in dic.items():
        while v.ndim > 2:
            v.squeeze_(0).squeeze_(-1)
        if v.ndim == 2:
            v.squeeze_(-1)
        new_dic[k] = v.view(-1, v.shape[-1]).tolist() if v.ndim > 1 else v.tolist()
    return new_dic


def post_process_data(merged_outputs, merged_dl1_params, dataset_parameters):
    """
    Post process data produced by the inference of a model on dl1 data to make them dl2 ready

    This updates a dataframe containing dl1 params, adding the DL2 params values

    Parameters
    ----------
    merged_outputs : pd.DataFrame
        merged outputs produced by the model at test time
    merged_dl1_params : pd.DataFrame
        corresponding merged dl1 parameters
    dataset_parameters :dict
        parameters used to instantiate dataset objects

    Returns
    -------
    pd.DataFrame
        dl2_params
    """
    particle_dict = dataset_parameters["particle_dict"]
    swapped_particle_dict = {v: k for k, v in particle_dict.items()}
    # Prepare data
    for param_name in ["mc_core_x", "mc_core_y", "tel_pos_x", "tel_pos_y", "tel_pos_z", "mc_x_max"]:
        if param_name in merged_dl1_params.columns:
            merged_dl1_params[param_name] *= 1000  # pass distances back in meters

    dl2_params = merged_dl1_params.copy(deep=True)

    for target in merged_outputs.columns:
        if target == "energy":
            dl2_params["reco_energy"] = 10 ** merged_outputs[target]
        if target == "xmax":
            dl2_params["reco_x_max"] = merged_outputs[target] * 1000
        if target == "impact":
            dl2_params[["reco_core_x", "reco_core_y"]] = pd.DataFrame(
                merged_outputs[target].tolist(), index=dl2_params.index
            )
            dl2_params["reco_core_x"] *= 1000
            dl2_params["reco_core_y"] *= 1000
            if dataset_parameters["group_by"] == "image":
                dl2_params["reco_core_x"] += dl2_params["tel_pos_x"]
                dl2_params["reco_core_y"] += dl2_params["tel_pos_y"]
        if target == "direction":
            dl2_params[["reco_alt", "reco_az"]] = pd.DataFrame(merged_outputs[target].tolist(), index=dl2_params.index)
            if dataset_parameters["group_by"] == "image":
                alt_tel = dl2_params["mc_alt_tel"] if "mc_alt_tel" in dl2_params.columns else dl2_params["alt_tel"]
                az_tel = dl2_params["mc_az_tel"] if "mc_az_tel" in dl2_params.columns else dl2_params["az_tel"]
                dl2_params["reco_alt"] += alt_tel
                dl2_params["reco_az"] += az_tel
        if target == "class":
            # network output is the output of a linear layer, we need to apply the softmax
            probabilities = torch.nn.functional.softmax(torch.tensor(list(merged_outputs[target].values)), dim=1)
            dl2_params["reco_particle"] = np.vectorize(swapped_particle_dict.get)(np.argmax(probabilities, 1))
            dl2_params["gammaness"] = probabilities[:, particle_dict[GAMMA_ID]]
            for k, v in particle_dict.items():
                dl2_params["reco_proba_{}".format(k)] = probabilities[:, v]

    return dl2_params


def write_dl2_file(dl2_params, dl1_dataset, output_path, mc_type=None, mc_energies=None):
    """
    Writes dl2 file from reconstructed dl2 params and dl1 dataset

    This opens the file of the dl1_dataset, copies what needs to be copied, and write the DL2 params from the dataframe
    """
    metadata = dl1_dataset.run_config["metadata"]
    if mc_type is not None:
        metadata["mc_type"] = mc_type
    metadata["GAMMALEARN_VERSION"] = runtime_version("gammalearn")
    # Copy dl1 info except images
    with tables.open_file(dl1_dataset.hdf5_file_path) as dl1:
        for node in dl1.walk_nodes():
            if not isinstance(node, tables.group.Group) and "image" not in node._v_pathname:
                stats = {"groups": 0, "leaves": 0, "links": 0, "bytes": 0, "hardlinks": 0}
                copy_leaf(
                    dl1_dataset.hdf5_file_path,
                    output_path,
                    node._v_pathname,
                    node._v_pathname,
                    title="",
                    filters=None,
                    copyuserattrs=True,
                    overwritefile=False,
                    overwrtnodes=True,
                    stats=stats,
                    start=None,
                    stop=None,
                    step=1,
                    chunkshape="keep",
                    sortby=None,
                    check_CSI=False,
                    propindexes=False,
                    upgradeflavors=False,
                    allow_padding=True,
                )
    # Write dl2 info
    if not dl1_dataset.simu:
        # Post dl2 ops for real data
        dl2_params = add_delta_t_key(dl2_params)
    write_dl2_dataframe(dl2_params, output_path)
    # Write metadata
    if mc_energies is not None:
        pd.DataFrame({"mc_trig_energies": np.array(mc_energies)}).to_hdf(output_path, key="triggered_events")
    with tables.open_file(output_path, mode="a") as file:
        for k, item in metadata.items():
            if k in file.root._v_attrs and type(file.root._v_attrs) is list:
                attribute = file.root._v_attrs[k].extend(metadata[k])
                file.root._v_attrs[k] = attribute
            else:
                file.root._v_attrs[k] = metadata[k]

class WriteDL2Files(Callback):
    """
    Callback to produce testing result data files
    TODO: do a real API to write DL2 files

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def on_test_end(self, trainer, pl_module):
        # Retrieve test data
        merged_outputs = pd.concat(
            [pd.DataFrame(prepare_dict_of_tensors(output)) for output in pl_module.test_data["output"]],
            ignore_index=True,
        )
        merged_dl1_params = pd.concat(
            [pd.DataFrame(prepare_dict_of_tensors(dl1)) for dl1 in pl_module.test_data["dl1_params"]],
            ignore_index=True,
        )

        dl2_params = post_process_data(merged_outputs, merged_dl1_params, pl_module.experiment.dataset_parameters)

        if pl_module.experiment.data_module_test is None or pl_module.experiment.merge_test_datasets:
            # Test has been done on the validation set or test dl1 have been merged in datasets by particle type

            ratio = pl_module.experiment.validating_ratio if pl_module.experiment.data_module_test is None else 1.0

            # Retrieve MC config information
            mc_configuration = {}

            def fetch_dataset_info(d):
                if isinstance(d, torch.utils.data.ConcatDataset):
                    for d_c in d.datasets:
                        fetch_dataset_info(d_c)
                elif isinstance(d, Subset):
                    fetch_dataset_info(d.dataset)
                elif issubclass(pl_module.experiment.dataset_class, BaseLSTDataset):
                    particle_type = d.dl1_params["mc_type"][0]
                    if particle_type not in mc_configuration:
                        mc_configuration[particle_type] = {"mc_energies": [], "run_configs": []}
                    if d.simu:
                        mc_energies = d.trig_energies
                        np.random.shuffle(mc_energies)
                        mc_energies = mc_energies[: int(len(mc_energies) * ratio)]
                        d.run_config["mcheader"]["n_showers"] *= ratio
                        mc_configuration[particle_type]["mc_energies"].extend(mc_energies)
                    mc_configuration[particle_type]["run_configs"].append(d.run_config)
                else:
                    pl_module.console_logger.error("Unknown dataset type, MC configuration cannot be retrieved")
                    raise ValueError

            for dataloader in trainer.test_dataloaders:
                fetch_dataset_info(dataloader.dataset)

            # Write one file per particle type
            for mc_type in mc_configuration:
                particle_mask = merged_dl1_params["mc_type"] == mc_type

                gb_file_path = (
                    pl_module.experiment.main_directory
                    + "/"
                    + pl_module.experiment.experiment_name
                    + "/"
                    + pl_module.experiment.experiment_name
                    + "_"
                    + str(mc_type)
                    + ".h5"
                )
                if os.path.exists(gb_file_path):
                    os.remove(gb_file_path)

                writer = HDF5TableWriter(gb_file_path)
                dl1_version = []
                ctapipe_version = []
                runlist = []

                for config in mc_configuration[mc_type]["run_configs"]:
                    try:
                        dl1_version.append(config["metadata"]["LSTCHAIN_VERSION"])
                    except Exception:
                        pl_module.console_logger.warning("There is no LSTCHAIN_VERSION in run config")
                    try:
                        ctapipe_version.append(config["metadata"]["CTAPIPE_VERSION"])
                    except Exception:
                        pl_module.console_logger.warning("There is no CTAPIPE_VERSION in run config")
                    try:
                        runlist.extend(config["metadata"]["SOURCE_FILENAMES"])
                    except Exception:
                        pl_module.console_logger.warning("There is no SOURCE_FILENAMES in run config")
                    try:
                        writer.write("simulation/run_config", config["mcheader"])
                    except Exception:
                        pl_module.console_logger.warning("Issue when writing run config")
                writer.close()

                try:
                    assert len(set(dl1_version)) == 1
                except AssertionError:
                    warning_msg = (
                        "There should be strictly one dl1 data handler version in dataset but there are {}".format(
                            set(dl1_version)
                        )
                    )
                    pl_module.console_logger.warning(warning_msg)
                    dl1_version = "Unknown"
                else:
                    dl1_version = dl1_version[0]

                try:
                    assert len(set(ctapipe_version)) == 1
                except AssertionError:
                    warning_msg = "There should be strictly one ctapipe version in dataset but there are {}".format(
                        set(ctapipe_version)
                    )
                    pl_module.console_logger.warning(warning_msg)
                    ctapipe_version = "Unknown"
                else:
                    ctapipe_version = ctapipe_version[0]

                try:
                    assert runlist
                except AssertionError:
                    pl_module.console_logger.warning("Run list is empty")

                metadata = {
                    "LSTCHAIN_VERSION": dl1_version,
                    "CTAPIPE_VERSION": ctapipe_version,
                    "mc_type": mc_type,
                    "GAMMALEARN_VERSION": runtime_version("gammalearn"),
                }

                with tables.open_file(gb_file_path, mode="a") as file:
                    for k, item in metadata.items():
                        if k in file.root._v_attrs and type(file.root._v_attrs) is list:
                            attribute = file.root._v_attrs[k].extend(metadata[k])
                            file.root._v_attrs[k] = attribute
                        else:
                            file.root._v_attrs[k] = metadata[k]
                    if runlist and "/simulation" in file:
                        file.create_array("/simulation", "runlist", obj=runlist)

                pd.DataFrame({"mc_trig_energies": np.array(mc_configuration[mc_type]["mc_energies"])}).to_hdf(
                    gb_file_path, key="triggered_events"
                )

                if mc_type == csts.REAL_DATA_ID:
                    # Post dl2 ops for real data
                    dl2_params = add_delta_t_key(dl2_params)

                write_dataframe(
                    merged_dl1_params[particle_mask], outfile=gb_file_path, table_path=dl1_params_lstcam_key
                )
                write_dl2_dataframe(dl2_params[particle_mask], gb_file_path)
        else:
            # Prepare output
            if pl_module.experiment.dl2_path is not None:
                output_dir = pl_module.experiment.dl2_path
            else:
                output_dir = pl_module.experiment.main_directory + "/" + pl_module.experiment.experiment_name + "/dl2/"
            os.makedirs(output_dir, exist_ok=True)
            dataset = trainer.test_dataloaders[0].dataset
            output_name = os.path.basename(dataset.hdf5_file_path)
            output_name = output_name.replace("dl1", "dl2")
            output_path = os.path.join(output_dir, output_name)
            if os.path.exists(output_path):
                os.remove(output_path)

            mc_type = merged_dl1_params["mc_type"][0]
            mc_energies = dataset.trig_energies

            write_dl2_file(dl2_params, dataset, output_path, mc_type=mc_type, mc_energies=mc_energies)        
            

def create_dl2_params(test_data: dict, dataset_parameters: dict) -> pd.DataFrame:
    merged_outputs = pd.concat(
        [pd.DataFrame(prepare_dict_of_tensors(output)) for output in test_data["output"]], ignore_index=True
    )
    merged_dl1_params = pd.concat(
        [pd.DataFrame(prepare_dict_of_tensors(dl1)) for dl1 in test_data["dl1_params"]], ignore_index=True
    )
    dl2_params = post_process_data(merged_outputs, merged_dl1_params, dataset_parameters)
    return dl2_params
