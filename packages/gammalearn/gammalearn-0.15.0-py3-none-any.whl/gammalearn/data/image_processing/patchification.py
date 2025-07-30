import logging
from typing import Tuple

import numpy as np
import pandas as pd
import pkg_resources
import torch
from ctapipe.instrument import CameraGeometry
from typing_extensions import deprecated


def get_centroids_from_patches(patches: torch.Tensor, geom: CameraGeometry) -> torch.Tensor:
    """
    Compute module centroid positions from patch indices and geometry. As the indices of the pixels within each module
    is known, it is possible de get the x and y coordinates through the geometry. The centroid is computed as the mean
    of the coordinates of the pixels within each module.
    Parameters
    ----------
    patches: (torch.Tensor) pixel indices for each patch, corresponding to pixel modules. For example, in the case of
    LSTCam with 1855 pixels grouped in modules of 7 pixels, patches is a tensor of size (265, 7).
    geom: (ctapipe.CameraGeometry) geometry
    Returns
    -------
    centroids: (torch.Tensor)
    """
    x = geom.pix_x.value.astype(np.float32)  # Get pixel x coordinates from geometry
    y = geom.pix_y.value.astype(np.float32)  # Get pixel y coordinates from geometry
    centroids = []
    for module in patches:  # LSTCam: 265 modules
        pix_x = x[module.numpy()]
        pix_y = y[module.numpy()]
        # Compute centroid as the mean of the x and y coordinates of the pixels within the module
        centroid_x = np.mean(pix_x)
        centroid_y = np.mean(pix_y)
        centroids.append([centroid_x, centroid_y])
    centroids = torch.from_numpy(np.array(centroids))  # LSTCam: torch.Size([265, 2])
    return centroids


def check_patches(
    patch_indices: torch.Tensor, patch_centroids: torch.Tensor, geom: CameraGeometry, width_ratio: float = 1.2
) -> None:
    """
    Check patch indices validity: check if all patches of a module are not too far away from the patch center

    This check is usefull to detect if the centroid position were computed with a wrong geometry

    Parameters
    ----------
    patch_indices (torch.Tensor): pixel indices for each patch, corresponding to pixel modules
    patch_centroids (torch.Tensor): position of the module centroids
    geom (ctapipe.CameraGeometry): geometry
    width_ratio (int): tolerance to check pixel distance to centroid
    Returns
    -------
    """
    x = geom.pix_x.value.astype(np.float32)  # Get pixel x coordinates from geometry
    y = geom.pix_y.value.astype(np.float32)  # Get pixel x coordinates from geometry
    radius = (geom.pixel_width[0].value.astype(np.float32) * width_ratio) ** 2
    distance_from_centroid = []
    # We check that each pixel in a module lies in a circle
    # of diameter pixel width * width_ratio around the module centroid
    for module, centroid in zip(patch_indices, patch_centroids):
        pix_x = x[module.numpy()]
        pix_y = y[module.numpy()]
        centroid_x = centroid[0].numpy()
        centroid_y = centroid[1].numpy()
        distance_from_centroid.append((pix_x - centroid_x) ** 2 + (pix_y - centroid_y) ** 2)
    distance_from_centroid = np.concatenate(distance_from_centroid, axis=0)
    assert (distance_from_centroid < radius).all(), "{} - {}".format(distance_from_centroid, radius)


def get_patch_indices_and_centroids_from_geometry(geom: CameraGeometry) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Compute patch indices and centroid positions from geometry.

    First try with the received geometry `geom`, and if doesn't work try with an old geometry from lstchain 0.7

    TODO: remove lstchain 0.7 geometry support ?

    Parameters
    ----------
    geom (ctapipe.CameraGeometry): geometry
    Returns
    -------
    patch_indices, patch_centroids: (torch.Tensor, torch.Tensor)
    """
    try:
        # Try with LSTCam geometry
        pixel_ids = torch.arange(geom.n_pixels)  # LSTCam has n_pixels=1855 pixels
        patch_indices = pixel_ids.view(-1, 7)  # torch.Size([265, 7]) Pixels are grouped in module of 7 pixels
        patch_centroids = get_centroids_from_patches(patch_indices, geom)
        check_patches(patch_indices, patch_centroids, geom, width_ratio=1.2)
    except AssertionError:
        # Try with geometry from files (lstchain_0.7)
        try:
            module_per_pixel_file = pkg_resources.resource_filename(
                "gammalearn", "data/module_id_per_pixel_lstchain_0.7.txt"
            )
            pixel_module_df = pd.read_csv(module_per_pixel_file, sep=" ")
            patch_indices = []
            for mod in set(pixel_module_df["mod_id"]):
                patch_indices.append(pixel_module_df["pix_id"][pixel_module_df["mod_id"] == mod].values)
            patch_indices = torch.tensor(np.stack(patch_indices, axis=0))
            patch_centroids = get_centroids_from_patches(patch_indices, geom)
            check_patches(patch_indices, patch_centroids, geom, width_ratio=1.2)
        except AssertionError as e:
            logging.warning("Unable to retrieve pixel modules from geometry")
            raise e
        else:
            return patch_indices, patch_centroids
    else:
        return patch_indices, patch_centroids


@deprecated("Transformers using interpolated images are deprecated and will be removed in a future version")
def check_grid(image_height: int, image_width: int, patch_size: int) -> None:
    """
    Check if the dimensions correspond before the step of patchification of the interpolated image.
    Check if the image can be exactly divided into patches, and there won't remain a part of the image not covered by patches

    Parameters
    ----------
    image_height: (int)
    image_width: (int)
    patch_size: (int)
    Returns
    -------
    """
    logger = logging.getLogger(__name__)

    try:
        assert image_height % patch_size == 0 or image_width % patch_size == 0
    except AssertionError as err:
        message = "The patch size ({patch_s}) must divide the image height ({img_h}) and width ({img_w}).".format(
            patch_s=patch_size, img_h=image_height, img_w=image_width
        )
        logger.exception(message)
        raise err


@deprecated("Transformers using interpolated images are deprecated and will be removed in a future version")
def get_patch_indices_and_grid(image_size: dict, patch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Compute the position of the pixels which belong to their respective patch and the grid.

    This is similar to `get_patch_indices_and_centroids_from_geometry` but can be used with an image
    that was interpolated on a 55x55 grid instead of using directly the pixel positions

    TODO: this was never used for experiment, only tested in CI

    Parameters
    ----------
    image_size: (dict) The shape of the image. In the case of IACT, the image must be interpolated on a regular grid.
    The dictionary must contain the following keys: 'height' and 'width'.
    patch_size: (int) The size of the patch. Patches are square so their height and width are similar.

    Returns
    -------
    patch_indices: (torch.Tensor) Tensor of size (n_patch, patch_size*patch_size), it indicates for each patch the
    coordinates of the pixels that it contains. For example, if the input image and the patches are respectively of size
    (55, 55) and (11, 11), patch_indices will be of size (25, 121) and the first row will contain [0, ..., 10, 55, ...].
    grid: (torch.Tensor) For example, if the input image and the patches are respectively of size (55, 55) and (11, 11),
    grid will be of size (25, 2).
    """
    # The height and width are passed as a dictionary in the model definition within the experiment setting file
    image_height, image_width = image_size["height"], image_size["width"]

    # Check if the dimensions correspond. Patches are not overlapping (it is neither an option), so the number of
    # patches and their size must correspond to the size of the image.
    check_grid(image_height, image_width, patch_size)

    # Compute the total number of patches
    n_patches_h, n_patches_w = (image_height // patch_size), (image_width // patch_size)
    n_patches = n_patches_h * n_patches_w

    # Compute patch indices: Taking for example an image and patches of respective size (55, 55) and (11, 11)
    pixel_ids = torch.arange(image_height * image_width)  # torch.Size([3025])
    pixel_ids = pixel_ids.view(-1, image_width)  # torch.Size([55, 55])
    patch_indices = pixel_ids.unfold(0, patch_size, patch_size).unfold(
        1, patch_size, patch_size
    )  # torch.Size([5, 5, 11, 11])
    patch_indices = patch_indices.flatten(start_dim=2)  # torch.Size([5, 5, 121])
    patch_indices = patch_indices.view(n_patches, -1)  # torch.Size([25, 121])

    # Compute patch grid: Taking for example an image and patches of respective size (55, 55) and (11, 11)
    grid_h = torch.arange(n_patches_h)  # torch.Size([5])
    grid_w = torch.arange(n_patches_w)  # torch.Size([5])
    grid = torch.meshgrid(grid_w, grid_h, indexing="ij")  # tuple(torch.Size([5, 5]) torch.Size([5, 5]))
    grid = torch.stack(grid, dim=0)  # torch.Size([2, 5, 5])
    grid = grid.reshape(2, -1).T  # torch.Size([2, 5, 5])

    # Convert the grid in torch.float
    grid = grid.to(torch.float)

    return patch_indices, grid
