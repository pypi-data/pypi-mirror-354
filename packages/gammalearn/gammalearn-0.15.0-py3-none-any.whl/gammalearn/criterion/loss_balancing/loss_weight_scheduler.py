import logging
import os

import numpy as np
import pandas as pd
import torch


class BaseW:
    """This class is inspired from the Pytorch LRScheduler that defines a learning rate scheduler.

    Analogically, the purpose of this class is to introduce a time-dependent loss/gradient weight.
    The module parameter is set within the 'gammalearn.experiment_runner.Experiment' class and provides the current and
    the max step information from the Pytorch Lightning Trainer that is involved in the training.

    It is an abstract class, the actual computation wrt time is performed in children classes in `self.function`

    Returns
    -------
    lambda_p (float): the step-dependent loss/gradient weight
    """

    def __init__(self):
        pass

    def function(self, p):
        return NotImplementedError

    def get_weight(self, trainer):
        if trainer is None:
            return 1.0
        else:
            current_step = trainer.fit_loop.total_batch_idx
            max_step = trainer.estimated_stepping_batches
            p = torch.tensor(current_step / max_step, dtype=torch.float32)  # Training progress (from 0 to 1)
            return self.function(p)


class ExponentialW(BaseW):
    """Compute the exponential weight corresponding to the domain adaptation loss weight.

    See [1]_

    This class is particularly useful when applied to the DANN 'grad_weight' argument but may also be applied in other
    context.

    Parameters
    ----------
    gamma : int
        The exponential coefficient in exp(-gamma*p).

    References
    ----------
    .. [1] Y. Ganin, "Domain-Adversarial Training of Neural Networks (DANN)", http://arxiv.org/abs/1705.07115

    Examples
    --------
    >>> # In more details, in the experiment setting file and in the case of DANN, this class can be used as follows:
    >>> targets = collections.OrderedDict({'domain_class': {..., 'grad_weight': ExponentialW(gamma=10), ..., }})
    """

    def __init__(self, gamma=10):
        super().__init__()
        self.gamma = torch.tensor(gamma, dtype=torch.float32)

    def function(self, p):
        return 2.0 / (1.0 + torch.exp(-self.gamma * p)) - 1.0


class DistributionW:
    """

    The class is used to apply a weight on the loss of an event, based on how frequent the energy of the event is in the
    total energy distribution. The goal is to apply bigger weight to events with energy that are less frequent.

    TODO: remove because it is not helping performances ?

    Parameters
    ----------
    path (str): the path to the csv file containing the distribution
    """

    def __init__(self, path: str) -> None:
        assert os.path.exists(path), "The distribution file {path} does not exist"
        logger = logging.getLogger(__name__)
        logger.debug(f"Loading distribution from {path}")
        self.distrib = pd.read_csv(path)

    def apply(self, loss: torch.Tensor, entry: torch.Tensor) -> torch.Tensor:
        loss_weighted = loss.clone()
        xp = self.distrib["x"].to_numpy()
        fp = self.distrib["y"].to_numpy()
        x = entry.cpu().numpy()
        fx = torch.from_numpy(np.interp(x, xp, fp))
        weights = fx.to(loss.device)
        loss_weighted = loss_weighted * weights

        return loss_weighted
