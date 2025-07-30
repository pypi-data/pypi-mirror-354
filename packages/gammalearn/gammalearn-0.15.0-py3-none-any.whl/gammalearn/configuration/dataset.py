from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from gammalearn.data.LST_dataset import FileLSTDataset, MemoryLSTDataset


class DatasetType(StrEnum):
    FILELSTDATASET = FileLSTDataset.__name__
    MEMORYLSTDATASET = MemoryLSTDataset.__name__


class DatasetConfiguration(BaseModel):
    """Abstract Configuration class for a dataset

    This class only defines the dataset_type field, which is used in the children classes
    to validate that the dataset type is indeed corresponding to the configuration class

    This is usefull to force the users to write the dataset class they want to use in the
    configuration, while still letting pydantic figure out which configuration class is
    been used.
    """

    # forbid extra fields, otherwise this configuration would match anything that has the same field
    model_config = ConfigDict(extra="forbid")

    dataset_type: DatasetType = Field(
        title="Dataset Type",
        description="Type of dataset to use to load the data.",
        examples=[dataset_type for dataset_type in DatasetType],
    )


def check_dataset_type(dataset_type: DatasetType, expected_value: str):
    if dataset_type != expected_value:
        raise ValueError(
            "dataset_type is {} but the dataset configuration matched the {} type".format(dataset_type, expected_value)
        )
    return dataset_type


class MemoryLSTDatasetConfiguration(DatasetConfiguration):
    """Configuration items of :py:class:`~gammalearn.data.LST_dataset.MemoryLSTDataset`"""

    # forbid extra fields, otherwise this configuration would match anything that has the same field
    model_config = ConfigDict(extra="forbid")

    # TODO: should probably be a litteral rather than any string, to catch errors early.
    # but didn't find yet in ctapipe where the camera types or names are defined...
    camera_type: str = Field(
        title="Camera Type",
        description="Camera type to use when loading the images geometry from files to process the images. To see "
        "available camera types, check ctapipe documentation",  # TODO: link to ctapipe documentation
        examples=[
            "LST_LSTCam"
        ],  # note: examples is a LIST of examples, so if only 1 example, still a list of 1 element
    )
    group_by: Literal["image", "event"] = Field(
        title="Event grouping key",
        description="Events in the datasets can be grouped together so that all images of the same event by several "
        "telescopes can be merged together. This is deprecated I believe and only grouping by image is supported, which "
        "doesn't group at all.",  # TODO: is this deprecated for real ?
        examples=[""],
    )
    use_time: bool = Field(
        title="Use Time Peak Map",
        description="If True, then the pixels peak time maps are concatenated to the charge images and used as input "
        "to the network",
        examples=[True, False],
        default=True,  # we pretty much always use time. However be very carefull with default arguments as they tend to either
        # change, and then running the config with an old program has different behaviour
        # be forgotten, and then people are left wondering how a certain value was set in the code while chasing after
        # a nasty bug
        # TODO: here, we'd be better off removing the configuration field and always use the time in the code.
    )
    # TODO: This is defined in gammalearn.configuration.constants, so should be removed from config ?
    # particle_dict: dict[str, int] = Field(
    #     title="Particle Class Dictionary",
    #     description="A dictionnary mapping a particle name (string) to a integer representing its class index for the "
    #     "network.",
    #     examples=[{"GAMMA": 0, "PROTON": 1}],
    # )
    # TODO/ what is this field ?
    # targets: str = Field(
    #     title="TODO",
    #     description="I don't remember what this is",
    #     examples=["???"],
    # )
    subarray: list[int] = Field(
        title="Subarray",
        description="Images of this subarray will be loaaded. The subarray is defined as a list of telescope ID "
        "included in the subarray, so for instance [1] selects the subarray with events of LST1.",  # TODO: probably deprecated as well
        examples=[[1], [1, 2, 3, 4]],
    )
    # TODO: define configuration classes for each of the fileters
    # TODO: determine if we need a dict[filtername, filterconfig] rather than a list, to help chose the right class to
    # validate the config (and check that the filter name is supported early in the validation)
    # TODO: we could also make it a list of literal, the literal been all the possible filter names
    # image_filters: None | list[IntersityFilterConfiguration | CleaningFilterConfiguration] = Field(
    #     title="Filters",
    #     description="Events whose images will not pass these filters will be removed from the dataset.",
    #     examples=[None],
    # )
    # TODO: event filters is the same than image filter, but filtering on parameters value instead of image array
    # event_filters: None | list[..., ...] = Field()

    # here example with list of literal. If we need to pass arguments to the transforms, we should implement the
    # geometry configuration classes, and change this to a dict ?
    transform: None | list[Literal["to_tensor", "normalize_pixel", "to_geometry?"]] = Field(  # any possible transform
        title="Image Transforms",
        description="Optional list of transformation to apply to the images, after they are loaded",
        examples=[None, ["to_tensor", "to_geometry"]],
    )
    # target transform is the same thing as transform, but transforms are applied to the labels, not in the input
    # target_transform: None | list[Literal["???", "????"]]

    check_dataset_type = field_validator("dataset_type", mode="plain")(
        lambda x: check_dataset_type(x, MemoryLSTDataset.__name__)
    )


# TODO: configuration class for the LST file dataset
class FileLSTDatasetConfiguration(DatasetConfiguration):
    # forbid extra fields, otherwise this configuration would match anything that has the same field
    model_config = ConfigDict(extra="forbid")

    check_dataset_type = field_validator("dataset_type", mode="plain")(
        lambda x: check_dataset_type(x, FileLSTDataset.__name__)
    )
