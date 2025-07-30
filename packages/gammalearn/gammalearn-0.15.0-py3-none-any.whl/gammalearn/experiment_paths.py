import logging
import os
import wandb

from pathlib import Path

from lightning import Callback
from gammalearn.gl_logging.net import LogWandb

class WriteData(Callback):
    """Generic function to find paths, prepare folders..."""

    # TODO: create a class that makes explicit the experiment files structure
    # example: https://gitlab.in2p3.fr/CTA-LAPP/rta/lst_auto_rta/-/blob/master/lst_auto_rta/paths.py?ref_type=heads

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = None
        self.output_file_default = None

    def get_output_path(self, experiment) -> Path:
        # Prepare output folder
        if experiment.output_dir is not None:
            output_dir = Path(experiment.output_dir)
        else:
            output_dir = Path(experiment.main_directory, experiment.experiment_name, self.output_dir_default)

        output_dir.mkdir(exist_ok=True)

        # Prepare output file
        if experiment.output_file is not None:
            output_file = Path(experiment.output_file)
        else:
            output_file = Path(self.output_file_default)

        # Get output path
        output_path = output_dir.joinpath(output_file)

        if output_path.exists():
            output_path.unlink()

        return output_path


def prepare_experiment_folder(main_directory, experiment_name):
    """
    Prepare experiment folder and check if already exists
    Parameters
    ----------
    main_directory (string)
    experiment_name (string)

    Returns
    -------

    """
    logger = logging.getLogger(__name__)
    experiment_directory = main_directory + "/" + experiment_name + "/"
    if not os.path.exists(experiment_directory):
        os.makedirs(experiment_directory)
        os.chmod(experiment_directory, 0o775)
    else:
        logger.info("The experiment {} already exists !".format(experiment_name))
    logger.info("Experiment directory: %s " % experiment_directory)


def get_wandb_checkpoint_path(checkpoint_path, root=None) -> str:
    """ Function to use and download model's artifact from gammalearn's wandb registry (https://wandb.ai/orgs/gammalearn-org/registry/)
        The checkpoint path to the downloaded model is returned.

    Parameters
    ----------
    checkpoint_path (str): An artifact path to the model checkpoint
    root (str): If specified, the model checkpoint will be downloaded in this directory.
    
    Returns
    -------
    checkpoint_path: The full path to the downloaded model checkpoint
    """
    run = wandb.init(job_type="download_model")
    artifact = wandb.use_artifact(checkpoint_path, type="model")
    artifact_dir = artifact.download(root=root)
    checkpoint_path = Path(artifact_dir).joinpath(next(iter(artifact.manifest.entries.keys())))
    run.finish()
    LogWandb.model_artifact_on_wandb = artifact
    return checkpoint_path