import numpy as np
from torchvision import transforms

from gammalearn.data.image_processing.noise_augmentation import (
    AddGaussianNoise,
    AddPoissonNoise,
    GetPoissonNoiseFromPedestals,
)


class GLearnCompose(transforms.Compose):
    """
    Custom transform Compose that can receive/output extra parameters of some transforms, when called.
    """

    def __call__(self, img, **kwargs):
        transform_params = {}
        for t in self.transforms:
            if isinstance(t, AddPoissonNoise):
                img = t(img, kwargs["simu"])
                transform_params["poisson_rate"] = t.rate_sampled
            elif isinstance(t, GetPoissonNoiseFromPedestals):
                img = t(img, kwargs["simu"], kwargs["pedestals"])
                transform_params["poisson_rate"] = t.rate_sampled
            elif isinstance(t, AddGaussianNoise):
                img = t(img)
                transform_params["gaussian_mean"] = t.mu_sampled
                transform_params["gaussian_std"] = t.sigma_sampled
            else:
                img = t(img)
        return img, transform_params


class FlattenNumpy(object):
    def __init__(self, start_dim=0):
        self.start_dim = start_dim

    def __call__(self, data):
        size = np.prod(data.shape[self.start_dim :])
        return data.reshape(data.shape[: self.start_dim] + tuple([size]))
