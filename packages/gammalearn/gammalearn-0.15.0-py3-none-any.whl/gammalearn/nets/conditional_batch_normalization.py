from typing import Tuple

import torch
import torch.nn as nn


class CBN(nn.Module):
    """
    Conditioned Batch Norm.
    From the article https://proceedings.neurips.cc/paper_files/paper/2017/file/6fab6e3aa34248ec1e34a4aeedecddc8-Paper.pdf
    Inspired from https://github.com/ap229997/Conditional-Batch-Norm/blob/master/model/cbn.py
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        self.input_size = input_size  # Size of the encoded conditional input
        self.hidden_size = hidden_size
        self.output_size = output_size  # Output of the MLP - for each channel

        self.device = None
        self.use_betas, self.use_gammas = True, True  # If False, classical Batch Norm 2d is applied
        self.batch_size, self.channels, self.height, self.width = None, None, None, None

        # Beta and gamma parameters for each channel - defined as trainable parameters
        self.betas, self.gammas = None, None

        # MLP used to predict betas and gammas
        self.fc_gamma = nn.Sequential(
            nn.Linear(self.input_size, self.hidden_size),
            nn.ReLU(inplace=True),
            nn.Linear(self.hidden_size, self.output_size),
        )

        self.fc_beta = nn.Sequential(
            nn.Linear(self.input_size, self.hidden_size),
            nn.ReLU(inplace=True),
            nn.Linear(self.hidden_size, self.output_size),
        )

        # Initialize weights using Xavier initialization and biases with constant value
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0.1)

    def create_cbn_input(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.use_betas:
            delta_betas = self.fc_beta(x)
        else:
            delta_betas = torch.zeros(self.batch_size, self.channels).to(self.device)

        if self.use_gammas:
            delta_gammas = self.fc_gamma(x)
        else:
            delta_gammas = torch.zeros(self.batch_size, self.channels).to(self.device)

        return delta_betas, delta_gammas

    def _set_parameters(self) -> None:
        if self.betas is None:
            self.betas = nn.Parameter(torch.zeros(self.batch_size, self.channels)).to(self.device)
        if self.gammas is None:
            self.gammas = nn.Parameter(torch.ones(self.batch_size, self.channels)).to(self.device)

    def forward(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """This method expects the noise level as an extra arguments in the kwargs
        TODO: Use noise level explicitely"""

        assert (
            "conditional_input" in kwargs.keys()
        ), "Encodded conditional input must be provided in the forward method if using CBN"
        conditional_input = kwargs["conditional_input"]
        self.device = x.device
        self.batch_size, self.channels, self.height, self.width = x.data.shape
        self._set_parameters()

        # Get delta values
        delta_betas, delta_gammas = self.create_cbn_input(conditional_input)

        betas_cloned = self.betas.clone()[: self.batch_size]  # In case batch size changes (e.g. last test batch)
        gammas_cloned = self.gammas.clone()[: self.batch_size]  # In case batch size changes (e.g. last test batch)

        # Update the values of beta and gamma
        betas_cloned += delta_betas
        gammas_cloned += delta_gammas

        # Extend the betas and gammas of each channel across the height and width of feature map
        betas_expanded = torch.stack([betas_cloned] * self.height, dim=2)
        betas_expanded = torch.stack([betas_expanded] * self.width, dim=3)

        gammas_expanded = torch.stack([gammas_cloned] * self.height, dim=2)
        gammas_expanded = torch.stack([gammas_expanded] * self.width, dim=3)

        # Normalize the feature map
        feature_normalized = (x - x.mean()) / torch.sqrt(x.var() + 1e-8)

        # Get the normalized feature map with the updated beta and gamma values
        out = torch.mul(feature_normalized, gammas_expanded) + betas_expanded

        return out
