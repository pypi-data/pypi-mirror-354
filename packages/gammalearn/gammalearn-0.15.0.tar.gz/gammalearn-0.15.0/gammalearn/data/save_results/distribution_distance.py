import pandas as pd
import torch
from torchmetrics import Accuracy

from gammalearn.experiment_paths import WriteData


class WriteADistance(WriteData):
    """
    Callback to produce testing result data files

    Writes the A distance (divergence between domains computed by a classifier) to a csv file.

    Parameters
    ----------
    trainer (Trainer)
    pl_module (LightningModule)

    Returns
    -------
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_dir_default = "a_distance_results"
        self.output_file_default = "a_distance.csv"

    def on_test_end(self, trainer, pl_module):
        # Get prediction
        predictions, targets = torch.empty((0,)), torch.empty((0,))
        for output, label in zip(pl_module.test_data["output"], pl_module.test_data["label"]):
            predictions = torch.hstack((predictions, torch.argmax(output["domain_class"], dim=1).cpu()))
            targets = torch.hstack((targets, label["domain_class"].cpu()))
        predictions, targets = predictions.flatten().to(torch.int64), targets.flatten().to(torch.int64)

        # Compute accuracy
        accuracy_metric = Accuracy(num_classes=2)

        # Compute a-distance
        accuracy = accuracy_metric(predictions, targets)
        error = 1.0 - accuracy
        a_distance = torch.abs(
            (2.0 * (1.0 - 2.0 * error)).mean()
        )  # distance is 0 when classifier converges to 0.5 accuracy
        output_df = pd.DataFrame({"accuracy": [accuracy.numpy()], "A_distance": [a_distance.numpy()]})

        # Get output path
        output_path = self.get_output_path(pl_module.experiment)

        # Write output dataframe
        output_df.to_csv(output_path, index=False)
