import os

import pandas as pd
import torch
from lightning import Callback

import gammalearn.data.save_results.utils as utils
from gammalearn.experiment_paths import WriteData


class WriteAutoEncoderDL1(Callback):
    """
    Callback to produce testing result data files

    Writes a h5 file with the L2 norm between the decoder reconstructed image and the label image

    TODO: why is the difference between this and WriteAutoEncoder ?

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def on_test_end(self, trainer, pl_module):
        # Set output dataframe
        output_df = pd.DataFrame()

        # Fill the output dataframe with the errors between the AE outputs and the ground truths
        merged_outputs = utils.merge_list_of_dict(pl_module.test_data["output"])  # TODO: output may be a dict
        for k, v in merged_outputs.items():
            output_df[k] = torch.cat(v).detach().to("cpu").numpy()

        # Also fill with the dl1 parameters if they are available
        merged_dl1_params = utils.merge_list_of_dict(pl_module.test_data["dl1_params"])
        for k, v in merged_dl1_params.items():
            if k in ["mc_core_x", "mc_core_y", "tel_pos_x", "tel_pos_y", "tel_pos_z", "mc_x_max"]:
                output_df[k] = 1000 * torch.cat(v).detach().to("cpu").numpy()
            else:
                output_df[k] = torch.cat(v).detach().to("cpu").numpy()

        # Get output path
        if pl_module.experiment.data_module_test is None:
            # Test has to be done on the validation set: Write one file
            output_path = os.path.join(
                pl_module.experiment.main_directory,
                pl_module.experiment.experiment_name,
                pl_module.experiment.experiment_name + "_ae_validation_results.h5",
            )
        else:
            # One output file per dl1 file
            output_dir = os.path.join(
                pl_module.experiment.main_directory, pl_module.experiment.experiment_name, "ae_test_results"
            )
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            dataset = trainer.test_dataloaders[0].dataset
            output_name = os.path.basename(dataset.hdf5_file_path)
            output_name = output_name.replace("dl1", "ae_results")
            output_path = os.path.join(output_dir, output_name)

        if os.path.exists(output_path):
            os.remove(output_path)

        # Write output dataframe
        output_df.to_hdf(output_path, key="data")


class WriteAutoEncoder(WriteData):
    """Callback to produce testing result data files

    Writes a h5 file with the L2 norm between the decoder reconstructed image and the label image

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = "ae_results"
        self.output_file_default = "ae.csv"

    def on_test_end(self, trainer, pl_module):
        # Compute error between the AE outputs and the ground truths
        error = torch.empty((0,))
        for output, label in zip(pl_module.test_data["output"], pl_module.test_data["label"]):
            prediction = output["autoencoder"]
            target = label["autoencoder"]
            error = torch.hstack((error, torch.pow(prediction - target, 2).mean().cpu()))

        # Compute the mean of the error
        output_df = pd.DataFrame({"MSE": error.mean().numpy()}, index=[0])

        # Get output path
        output_path = self.get_output_path(pl_module.experiment)

        # Write output dataframe
        output_df.to_csv(output_path, index=False)
