from typing import Sequence

import numpy as np

from gammalearn.data.LST_dataset import BaseLSTDataset


def intensity_filter(
    dataset: BaseLSTDataset,
    intensity: Sequence[float | None],
):
    """Compute a mask to filter a LST Dataset based on image intensity

    Parameters
    ----------
    dataset : BaseLSTDataset
        The LST Dataset to filter
    intensity : Sequence[float  |  None]
        Sequence of 2 floats, an image will be filtered out if the intensity is not in the range
        ``[intensity[0], intensity[1]]``. Values can also be None, in which case they will be set to ±np.inf.

    Returns
    -------
    np.ndarray
        Boolean array True if the image is to be kept, False if the image is to be filtered out

    Raises
    ------
    ValueError
        If `intensity` is not a sequence of 2 floats.
    ValueError
        If `intensity` lower range is greater than `intensity` higher range
    """

    if len(intensity) != 2:
        raise ValueError(
            "Intensity should be a sequnce of 2 floats, but got {} with length {}".format(intensity, len(intensity))
        )

    pe_min = intensity[0] if intensity[0] is not None else -np.inf
    pe_max = intensity[1] if intensity[1] is not None else np.inf

    if intensity[0] > intensity[1]:
        raise ValueError("Intensity lower range {} is greater to intensity higher range {}!".format(pe_min, pe_max))

    return (pe_min < dataset.dl1_params["intensity"]) & (dataset.dl1_params["intensity"] < pe_max)
