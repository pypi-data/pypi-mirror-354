"""
Data Volume Reduction (dvr) is a preprocessing applied on real data on DL1.
The following functions are meant to replicate this preprocessing.
The real implementation is done using lstchain package v0.10.4
https://github.com/cta-observatory/cta-lstchain/blob/main/lstchain/scripts/lstchain_dvr_pixselector.py
"""

import numpy as np

# Parameters used in the lstchain implementation
NUMBER_DILATIONS = 1
CHARGE_THRESHOLD = 8.0
MIN_NUMBER_PIXELS = 500


def get_selected_pixels(
    charge_map, min_charge_for_certain_selection, number_of_rings, geom, min_npixels_for_full_event=MIN_NUMBER_PIXELS
):
    """
    Function to select the pixels which likely contain a Cherenkov signal

    Parameters
    ----------
    charge_map : ndarray
        pixel-wise charges in photo-electrons

    min_charge_for_certain_selection : float
        pixels above this charge will be selected

    number_of_rings : int
        number of "rings" of pixels around the pixels selected by
        their charge that will also be selected (N=1 means just the immediate
        neighbors; N=2 adds the neighbors of neighbors and so on)

    geom: CameraGeometry
        camera geometry

    min_npixels_for_full_event: int, optionnal
        full camera will be selected for events with
        more than this number of pixels passing the standard selection

    Returns
    -------
    ndarray (boolean):
        mask containing the selected pixels

    Notes:
    ------
    This function is replicated from lstchain implementation v0.10.4
    (https://github.com/cta-observatory/cta-lstchain/blob/main/lstchain/scripts/lstchain_dvr_pixselector.py)

    """

    # Proceed with the identification of interesting pixels to be saved.
    # Keep pixels that have a charge above min_charge_for_certain_selection:
    selected_pixels = charge_map > min_charge_for_certain_selection

    # Add "number_of_rings" rings of pixels around the already selected ones:
    for ring in range(number_of_rings):
        # we add-up (sum) the selected-pixel-wise map of neighbors, to find
        # those who appear at least once (>0). Those should be added:
        additional_pixels = np.sum(geom.neighbor_matrix[selected_pixels], axis=0) > 0
        selected_pixels |= additional_pixels

    # if more than min_npixels_for_full_event were selected, keep whole camera:
    if selected_pixels.sum() > min_npixels_for_full_event:
        selected_pixels = np.array(geom.n_pixels * [True])

    return selected_pixels
