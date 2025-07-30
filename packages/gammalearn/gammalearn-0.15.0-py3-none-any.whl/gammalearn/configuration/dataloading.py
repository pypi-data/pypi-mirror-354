from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from gammalearn.configuration.dataset import FileLSTDatasetConfiguration, MemoryLSTDatasetConfiguration


class DataloadingConfiguration(BaseModel):
    """Configuration items of the data loading of an experiment"""

    # forbid extra fields, otherwise this configuration would match anything that has the same field
    model_config = ConfigDict(extra="forbid")

    data_directories: list[Path] = Field(
        title="Data Directories",
        description="List of directories containing the input data. All hdf5 files in the directories will be loaded.",
        examples=["/path/to/data/dir"],
    )
    batch_size: int = Field(
        title="Batch Size",
        description="Size of the input batches to build from the data. If the input batch "
        "(and model gradients if training) don't fit in the gpu RAM, a CUDA out of memory error will be raised. "
        "One LST is typically 55x55x2x4 + 20x4 bytes (55x55 image, + peak times, + 20 parameters, floats)",
        examples=[256, 4096],
    )
    preprocessing_workers: None | int = Field(
        title="Number of Preprocessing Workers",
        description="Number of preprocessing processes to use to load the data while creating the datasets. 7 for 1 gpu ?",
        examples=[0, 2, 7],
    )
    dataloader_workers: None | int = Field(
        title="Dataloader workers",
        description="Number of processes to use to assemble the batches. See pytorch DataLoader.",
        examples=[0, 7],
    )
    dataset_size: None | int = Field(
        title="Maximum Dataset Size",
        description="If this value is set, the dataset will be limited to the first `dataset_size` events.",  # TODO: first of randomly selected ?
        examples=[None, 2000],
        default=None,  # ok to have default here, this is mostly a debugging option
    )
    files_max_number: None | int = Field(
        title="Maximum File Number",
        description="If this value is set, the datasets will only be created for `files_max_number` files and the "
        "remaining files will be ignored. This can be set to 1 or 2 to quickly debug an experiment as it reduces a lot "
        "the time spend loading the data.",
        examples=[None, 1],
        default=None,
    )
    dataset_parameters: FileLSTDatasetConfiguration | MemoryLSTDatasetConfiguration = Field(
        title="Dataset Configuration",
        description="Configuration items to pass to the dataset class.",
        examples=[FileLSTDatasetConfiguration(dataset_type="FileLSTDataset")],
    )
