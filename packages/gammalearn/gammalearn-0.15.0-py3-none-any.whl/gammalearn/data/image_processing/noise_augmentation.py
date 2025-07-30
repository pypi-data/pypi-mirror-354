from typing import Tuple

import numpy as np
import torch


class AddPoissonNoise(object):
    """
    Add a noise sampled from a Poisson distribution to the pixel charges.
    The noise is sampled from a Poisson distribution with a rate defined by the user.
    This transform can also be used in the heterogeneous case that the data contains both real and simulated data.
    If the __call__() method contains the 'simu' variable set to False, the noise is not added to the data. It is set to
    True by default. If the GLearnCompose is used, it is set to False for real data.

    Parameters
    ----------
    rate (float or list): the rate of the Poisson distribution. If a list, the rate is sampled from a uniform
    distribution between the two values (list only has 2 values).
    """

    def __init__(self, rate: list):
        rate = rate if isinstance(rate, list) else [rate]
        assert all(isinstance(r, float) for r in rate), "The rate list must contain only floats."
        assert 1 <= len(rate) <= 2, "The rate list must contain either one (rate) or two (min and max) elements."
        self.rate = rate

    def sample_rate(self) -> float:
        if len(self.rate) == 2:
            return np.random.uniform(self.rate[0], self.rate[1])
        else:
            return self.rate

    def compute_noise(self, data: np.ndarray) -> np.ndarray:
        self.rate_sampled = torch.tensor([self.sample_rate()], dtype=torch.float32)
        poisson = torch.distributions.poisson.Poisson(self.rate_sampled)
        if data.ndim == 1:
            sample_shape = torch.Size(list(data.shape))
        elif data.ndim == 2:
            sample_shape = torch.Size(list(data[0].shape))
        return poisson.sample(sample_shape=sample_shape).numpy()

    def apply_noise(self, data: np.ndarray, noise: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data + noise
        elif data.ndim == 2:
            data[0] = data[0] + noise.T  # Apply noise to the charge image
        return data

    def __call__(self, data: np.ndarray, simu: bool) -> np.ndarray:
        if simu:
            noise = self.compute_noise(data)
            return self.apply_noise(data, noise)
        else:  # Real data
            noise = self.compute_noise(data)  # Set the rate_sampled attribute, but do not apply the noise
            return data


class GetPoissonNoiseFromPedestals(object):
    """
    Get a noise from the pedestals within a subrun. The sampled rate corresponds to the difference between the trained
    Monte Carlo noise rate and the rate computed from the pedestals images
    δλ = λ_pedestals - λ_mc > 0

    The goal is to use during CBN inference on real data:
        - read noise level from pedestals
        - populate the self.rate_sampled of this class
        - this member will be used to pass the value to the CBN layers of the models as the conditioning variable.
            - this is done in 2 steps: in the glearnCompose, the rate_sampled are put in the forward_kwargs of the batch
            - the CBN module reads the batch forward_kwargs to get the values

    Parameters
    ----------
    rate_mc (float or list): the rate of the Poisson distribution. If a list, the rate is sampled from a uniform
    distribution between the two values.
    """

    def __init__(self, rate_mc: float):
        assert isinstance(rate_mc, float), "The rate must be a float."
        self.rate_mc = rate_mc  # λ_mc
        self.rate_sampled = torch.tensor([0], dtype=torch.float32)  # δλ

    def compute_rate_from_pedestals(self, pedestals: np.ndarray) -> None:
        # The rate is the average value of the pedestals (all pixels) events of a sub-run
        if pedestals is not None:
            rate_real = np.mean(pedestals)
            rate_sampled = rate_real - self.rate_mc
            self.rate_sampled = torch.tensor([rate_sampled], dtype=torch.float32)

    def __call__(self, data: np.ndarray, simu: bool, pedestals: np.ndarray) -> np.ndarray:
        if not simu:  # Real data: compute rate
            self.compute_rate_from_pedestals(pedestals)
        return data


class AddGaussianNoise(object):
    """
    Same thing than AddPoissonNoise but with a gaussian noise. Only used for digits dataset.

    Add a noise sampled from a Gaussian distribution to the image.
    The noise is sampled from a Gaussian distribution with a mean and standard deviation defined by the user.

    Parameters
    ----------
    mu (float or list): the mean of the Gaussian distribution. If a list, the rate is sampled from a uniform
    distribution between the two values.
    sigma (float or list): the stadard deviation of the Gaussian distribution. If a list, the rate is sampled
    from a uniform distribution between the two values.
    """

    def __init__(self, mu: list, sigma: list):
        mu = mu if isinstance(mu, list) else [mu]
        sigma = sigma if isinstance(sigma, list) else [sigma]
        assert all(isinstance(m, float) for m in mu), "The mu list must contain only floats."
        assert all(isinstance(s, float) for s in sigma), "The sigma list must contain only floats."
        assert 1 <= len(mu) <= 2, "The mu list must contain either one (mu) or two (min and max) elements."
        assert 1 <= len(sigma) <= 2, "The sigma list must contain either one (sigma) or two (min and max) elements."
        self.mu = mu
        self.sigma = sigma

    def sample(self) -> Tuple[float, float]:
        if len(self.mu) == 2:
            mu = np.random.uniform(self.mu[0], self.mu[1])
        else:
            mu = self.mu

        if len(self.sigma) == 2:
            sigma = np.random.uniform(self.sigma[0], self.sigma[1])
        else:
            sigma = self.sigma

        return torch.tensor(mu, dtype=torch.float32).view(-1, 1), torch.tensor(sigma, dtype=torch.float32).view(-1, 1)

    def compute_noise(self, data: torch.Tensor) -> torch.Tensor:
        self.mu_sampled, self.sigma_sampled = self.sample()
        sample_shape = torch.Size(data.shape)
        if self.mu_sampled == self.sigma_sampled == 0.0:
            # This case triggers an error with the Normal class from Pytorch
            return torch.zeros_like(data)
        else:
            gaussian = torch.distributions.normal.Normal(self.mu_sampled, self.sigma_sampled)
            return gaussian.sample(sample_shape=sample_shape).view(sample_shape)

    def apply_noise(self, data: torch.Tensor, noise: torch.Tensor) -> torch.Tensor:
        return data + noise

    def __call__(self, data: torch.Tensor, **kwargs) -> torch.Tensor:
        noise = self.compute_noise(data)
        return self.apply_noise(data, noise)
