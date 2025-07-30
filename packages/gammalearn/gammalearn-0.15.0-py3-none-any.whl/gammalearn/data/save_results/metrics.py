import numpy as np
import pandas as pd
import torch
from torchmetrics import Accuracy, ConfusionMatrix

from gammalearn.configuration.constants import SOURCE, TARGET
from gammalearn.experiment_paths import WriteData


class WriteAccuracy(WriteData):
    """
    Callback to produce testing result data files

    logs the classification (gamma/proton) accuracy

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = "accuracy_results"
        self.output_file_default = "accuracy.csv"

    def on_test_end(self, trainer, pl_module):
        # Get prediction and ground truth
        predictions, targets = torch.empty((0,)), torch.empty((0,))
        for output, label in zip(pl_module.test_data["output"], pl_module.test_data["label"]):
            predictions = torch.hstack((predictions, torch.argmax(output["class"], dim=1).cpu()))
            targets = torch.hstack((targets, label["class"].cpu()))
        predictions, targets = predictions.flatten().to(torch.int64), targets.flatten().to(torch.int64)

        # Compute accuracy
        num_classes = pl_module.experiment.targets["class"]["output_shape"]
        accuracy = Accuracy(num_classes=num_classes, multiclass=True, average=None)
        output_df = pd.DataFrame({"Accuracy": accuracy(predictions, targets).numpy()}, index=[np.arange(num_classes)])

        # Get output path
        output_path = self.get_output_path(pl_module.experiment)

        # Write output dataframe
        output_df.to_csv(output_path, index=False)


class WriteAccuracyDomain(WriteData):
    """
    Callback to produce testing result data files

    logs the domain classifier (source/target) accuracy

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = "accuracy_domain_results"
        self.output_file_default = "accuracy_domain.csv"

    def on_test_end(self, trainer, pl_module):
        # Get prediction and ground truth
        predictions = torch.empty((0,))
        for output in pl_module.test_data["output"]:
            predictions = torch.hstack((predictions, torch.argmax(output["domain_class"], dim=1).cpu()))
        predictions = predictions.flatten().to(torch.int64)
        labels_source = (torch.ones(predictions.shape) * SOURCE).to(torch.int64)
        labels_target = (torch.ones(predictions.shape) * TARGET).to(torch.int64)

        # Compute accuracy
        num_classes = 2
        accuracy = Accuracy(num_classes=num_classes, task="multiclass")
        output_df = pd.DataFrame(
            [
                {"Accuracy source": accuracy(predictions, labels_source).numpy()},
                {"Accuracy target": accuracy(predictions, labels_target).numpy()},
            ],
            index=[np.arange(2)],
        )

        # Get output path
        output_path = self.get_output_path(pl_module.experiment)

        # Write output dataframe
        output_df.to_csv(output_path, index=False)


class WriteConfusionMatrix(WriteData):
    """
    Callback to produce testing result data files

    Log the confusion matrix of the classification

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = "confusion_matrix_results"
        self.output_file_default = "confusion_matrix.csv"

    def on_test_end(self, trainer, pl_module):
        # Get prediction and ground truth
        predictions, targets = torch.empty((0,)), torch.empty((0,))
        for output, label in zip(pl_module.test_data["output"], pl_module.test_data["label"]):
            predictions = torch.hstack((predictions, torch.argmax(output["class"], dim=1).cpu()))
            targets = torch.hstack((targets, label["class"].cpu()))
        predictions, targets = predictions.flatten().to(torch.int64), targets.flatten().to(torch.int64)

        # Compute accuracy
        num_classes = pl_module.experiment.targets["class"]["output_shape"]
        cm = ConfusionMatrix(num_classes=num_classes)
        output_df = pd.DataFrame(
            cm(predictions, targets).numpy(), index=[np.arange(num_classes)], columns=np.arange(num_classes)
        )

        # Get output path
        output_path = self.get_output_path(pl_module.experiment)

        # Write output dataframe
        output_df.to_csv(output_path, index=False)
