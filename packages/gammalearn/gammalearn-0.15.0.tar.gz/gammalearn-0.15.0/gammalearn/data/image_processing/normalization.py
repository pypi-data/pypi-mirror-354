import numpy as np
from ctapipe.image import tailcuts_clean


class ReducePixelValue(object):
    """Normalize a batch of image per channel (so time and charge aren't mixed)
    typically used with auto-encoders and transformers.
    """

    def __call__(self, data):
        if data.ndim == 1:  # only use charge, no time
            data = data / data.max()
        elif data.ndim == 2:  # use charge and time, normalize independently
            data[0] = data[0] / data[0].max()
            data[1] = data[1] / data[1].max()
        return data


def center_time(dataset, **opts):
    """
    Center pixel time based on the max intensity pixel

    ie: put the time for pixel with max value at t=0, and adapt the other times to match

    Parameters
    ----------
    dataset: `Dataset`

    Returns
    -------
    indices: `numpy.array`
    """
    geom = dataset.camera_geometry

    def clean(img):
        return tailcuts_clean(geom, img, **opts)

    clean_mask = np.apply_along_axis(clean, 1, dataset.images)

    cleaned = dataset.images * clean_mask
    max_pix = cleaned.argmax(axis=1)
    for i, times in enumerate(dataset.times):
        times -= times[max_pix[i]]
