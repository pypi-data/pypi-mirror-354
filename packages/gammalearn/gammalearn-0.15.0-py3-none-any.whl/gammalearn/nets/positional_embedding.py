import logging

import numpy as np
import torch
from typing_extensions import deprecated


def calculate_pos_emb(embed_dim: int, positions: torch.Tensor) -> torch.Tensor:
    """
    Compute the positional embedding. It corresponds to the spatial information of the image tokens.

    see MAE paper https://arxiv.org/abs/2111.06377

    Parameters
    ----------
    embed_dim: (int)
    positions: (torch.Tensor)
    Returns
    -------
    pos_embed: (torch.Tensor)
    """
    omega = torch.arange(embed_dim // 4) / (embed_dim / 4.0)
    omega = 1.0 / 10000**omega
    sin_x = torch.sin(torch.mm(positions[:, 0].unsqueeze(1), omega.unsqueeze(0)))
    cos_x = torch.cos(torch.mm(positions[:, 0].unsqueeze(1), omega.unsqueeze(0)))
    sin_y = torch.sin(torch.mm(positions[:, 1].unsqueeze(1), omega.unsqueeze(0)))
    cos_y = torch.cos(torch.mm(positions[:, 1].unsqueeze(1), omega.unsqueeze(0)))
    pos_embed = torch.cat([sin_x, cos_x, sin_y, cos_y], dim=1)

    return pos_embed


def add_tokens_to_pos_embed(
    pos_embed: torch.Tensor, additional_tokens: list, add_pointing: bool, embed_dim: int
) -> torch.Tensor:
    """
    Add the additional tokens positional embedding listed in the 'additional_tokens' in the current 'pos_embed'.
    Additional tokens embeddings are defined as a vector [i, i, ..., i] of size (1, embed_dim) to give them a greater
    distance from the image tokens.

    This can be used to add the pointing information as a positional embedding. It is a way to do multi-modality
    (like CBN) but for transformers, via the positional embedding.

    The pointing positional embedding is added here, but other embeddings can be added in the network. One could add
    the mean value of the pedestal for the subrun for instance, as another embedding.

    The additional embeddings are concatenated to the positional embedding, and in BaseMaskedAutoEncoder forward,
    the right values are retrieved to make the tokens to pass to the encoder.

    Parameters
    ----------
    pos_embed: (torch.Tensor) The current embedded vector.
    additional_tokens: (list) The list of additional tokens to be added.
    add_pointing: (bool) Whether add an additional pointing token.
    embed_dim: (int) The dimension of the embedding space.
    Returns
    -------
    pos_embed: (torch.Tensor) The new embedded vector.
    """
    additional_tokens = [] if additional_tokens is None else additional_tokens
    additional_tokens = additional_tokens + ["pointing"] if add_pointing else additional_tokens

    if additional_tokens is not None:
        try:
            assert isinstance(additional_tokens, list), "Please provide additional tokens as a list"
            for i in reversed(range(len(additional_tokens))):
                token = torch.full((1, embed_dim), i)
                pos_embed = torch.cat([token, pos_embed], dim=0)
        except TypeError:
            logging.warning("Additional tokens not used")

    return pos_embed


def get_2d_sincos_pos_embedding_from_patch_centroids(
    centroids: torch.Tensor, embed_dim: int, additional_tokens: list = None, add_pointing: bool = False
) -> torch.Tensor:
    """
    Compute 2d sincos positional embedding from pixel module centroid positions. Used for LST image.
    Parameters
    ----------
    centroids: (torch.Tensor) x and y position of pixel module centroids
    embed_dim: (int) dimension of embedding
    additional_tokens: (list) list of additional tokens for which add an embedding
    add_pointing: (bool) Whether add an additional pointing token.
    Returns
    -------
    torch.Tensor
    """
    # Rescale centroids to get closer to classical 2d image grid
    y_width = np.ptp(centroids[:, 1])  # peak to peak
    ratio = np.sqrt(len(centroids)) / y_width
    centroids[:, 0] -= centroids[:, 0].min()
    centroids[:, 1] -= centroids[:, 1].min()
    centroids *= ratio

    pos_embed = calculate_pos_emb(embed_dim, centroids)  # torch.Size([n_patches, embed_dim])

    return add_tokens_to_pos_embed(pos_embed, additional_tokens, add_pointing, embed_dim)


@deprecated("Transformers using interpolated images are deprecated and will be removed in a future release!")
def get_2d_sincos_pos_embedding_from_grid(
    grid: torch.Tensor, embed_dim: int, additional_tokens: list = None, add_pointing: bool = False
) -> torch.Tensor:
    """
    Compute the positional embedding from the grid. Used for interpolated images.
    """
    pos_embed = calculate_pos_emb(embed_dim, grid)

    return add_tokens_to_pos_embed(pos_embed, additional_tokens, add_pointing, embed_dim)
