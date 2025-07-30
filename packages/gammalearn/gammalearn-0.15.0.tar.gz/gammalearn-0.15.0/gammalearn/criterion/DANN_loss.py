import torch

from gammalearn.criterion.multitask import DomainConditionalLoss


class DANNLoss(DomainConditionalLoss):
    """
    Implementation of the Domain Adversarial Neural Networl (DANN) loss.
    From the DANN article https://arxiv.org/abs/1505.07818.

    Parameters
    ----------
    training_class : dict
        The dict of all the classes that trigger the training of the domain classifier. If set to
        None, no domain conditional is applied. In the LST dataset, MC labels are processed using the particle dictionary
        defined in the experiment settings, however the real labels remain the same.
    """

    def __init__(self, training_class: list = None):
        super().__init__(training_class=training_class)
        self.criterion = torch.nn.CrossEntropyLoss(reduction="none")

    def forward(self, output: torch.Tensor, labels: torch.Tensor):
        """
        DANN loss function.

        Parameters
        ----------
        output: (torch.Tensor) The model's output.
        labels: (torch.Tensor) The ground truth domain labels.
        """
        loss = self.criterion(output, labels)
        if self.loss_domain_mask is not None and self.domain_conditional:
            # mask = self.loss_domain_mask.to(output.device)
            mask = torch.cat([self.get_source_mask(), self.get_source_mask()]).to(output.device)
            loss = (loss * mask).sum() / mask.sum() if mask.sum() > 0 else torch.tensor(0.0, device=loss.device)

        return loss
