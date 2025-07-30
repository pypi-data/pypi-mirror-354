import numpy as np
from ctapipe.image import tailcuts_clean

from gammalearn.data.image_processing.image_interpolation import TransformIACT


class CleanImages(TransformIACT):
    """
    Cleaning transform: compute a cleaning mask using lstchain and apply it.
    Parameters
    ----------
    new_channel (Bool): if True, adds the cleaning mask to the data as a new channel.
    If False, apply the cleaning mask to the data.
    """

    def __init__(self, new_channel=False, **opts):
        self.opts = opts
        self.new_channel = new_channel
        self.camera_geometry = None

    def setup_geometry(self, camera_geometry):
        self.camera_geometry = camera_geometry

    def __call__(self, data):
        image = data if data.ndim == 1 else data[0]
        clean_mask = tailcuts_clean(self.camera_geometry, image, **self.opts)
        if self.new_channel:
            return np.concatenate([data, np.expand_dims(clean_mask, axis=0).astype(np.float32)])
        else:
            return data * clean_mask
