import os

from lightning.pytorch.loggers import TensorBoardLogger, WandbLogger

from gammalearn.gl_logging.net import LogModelParameters


class TrainerLogger:
    """
    The TrainerLogger class is used to define the logger used by the Pytorch Lightning Trainer.

    Used as a common class, specialized by the wandb and tensorboard logger

    """

    def __init__(self) -> None:
        pass

    def setup(self, experiment, gl_lightning_module) -> None:
        return NotImplementedError

    def get_log_directory(self, experiment) -> str:
        return os.path.join(experiment.main_directory, "runs")

    def get_run_directory(self, experiment) -> str:
        return os.path.join(self.get_log_directory(experiment), experiment.experiment_name)

    def create_directory(self, directory) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.chmod(directory, 0o775)


class TrainerTensorboardLogger(TrainerLogger):
    """
    The TrainerTensorboardLogger is a wrapper around the TensorBoardLogger class.
    It is used to define the logger used by the Pytorch Lightning Trainer, based on Tensorboard.
    """

    def __init__(self) -> None:
        super().__init__()
        self.type = "TensorBoardLogger"

    def setup(self, experiment, gl_lightning_module) -> None:
        """Setup the lightning tensorboard logger to the right folder"""
        run_directory = self.get_run_directory(experiment)
        self.create_directory(run_directory)
        self.logger = TensorBoardLogger(self.get_log_directory(experiment), experiment.experiment_name)


class TrainerWandbLogger(TrainerLogger):
    """
    The TrainerWandbLogger is a wrapper around the WandbLogger class.
    It is used to define the logger used by the Pytorch Lightning Trainer, based on Weights and Biases.
    More info at https://docs.wandb.ai/guides/integrations/lightning.
    """

    def __init__(self, offline: bool = False) -> None:
        super().__init__()
        self.offline = offline
        self.type = "WandbLogger"

    def setup(self, experiment, gl_lightning_module) -> None:
        """Setup the wandb logger in the right directory, passing the metadata like project, entity that are read from the settings file"""
        run_directory = self.get_run_directory(experiment)
        self.create_directory(run_directory)
        self.logger = WandbLogger(
            save_dir=run_directory, config=self.create_config(experiment), **self.create_parameters(experiment)
        )
        if LogModelParameters in experiment.training_callbacks:
            self.logger.watch(gl_lightning_module.net, log="all", log_freq=experiment.log_every_n_steps)
            experiment.training_callbacks().remove(LogModelParameters)

    def create_config(self, experiment) -> dict:
        return {
            "random_seed": experiment.random_seed,
            "epochs": experiment.max_epochs,
            "learning_rate": experiment.optimizer_parameters["network"]["lr"],
            "batch_size": experiment.batch_size,
        }

    def create_parameters(self, experiment) -> dict:
        return {
            "project": experiment.project,
            "entity": experiment.entity,
            "name": experiment.experiment_name + "_train",
            "tags": experiment.tags,
            "notes": experiment.info,
            "log_model": False, #Model is logged in the custom callback LogWandb() along with metadata and other run's artifacts.
            "offline": self.offline,  # can be used to use this logger in a node that doesn't have internet
        }
