import numpy as np
import torch


def fetch_dataset_geometry(dataset):
    if isinstance(dataset, torch.utils.data.Subset):
        return fetch_dataset_geometry(dataset.dataset)
    elif isinstance(dataset, torch.utils.data.ConcatDataset):
        return fetch_dataset_geometry(dataset.datasets[0])
    else:
        return dataset.camera_geometry


class WrongGeometryError(Exception):
    pass


def get_index_matrix_from_geom(camera_geometry):
    """
    Compute the index matrix from a ctapipe CameraGeometry

    Parameters
    ----------
    camera_geometry: `ctapipe.instrument.CameraGeometry`

    Returns
    -------
    indices_matrix: `numpy.ndarray`
        shape (n, n)

    """
    hex_to_rect_map = camera_geometry._pixel_indices_cartesian
    # ctapipe now uses np.iinfo(np.int32).min for invalid value, but gammalearn uses -1
    hex_to_rect_map[hex_to_rect_map < 0] = -1.0
    return np.rot90(hex_to_rect_map, k=-1).astype(np.float32)


def get_camera_layout_from_geom(camera_geometry):
    """
    From a ctapipe camera geometry, compute the index matrix and the camera layout (`Hex` or `Square`) for indexed conv

    Parameters
    ----------
    camera_geometry: `ctapipe.instrument.CameraGeometry`

    Returns
    -------
    tensor_matrix: `torch.Tensor`
        shape (1, 1, n, n)
    camera_layout: `str`
        `Hex` or `Square`

    """
    index_matrix = get_index_matrix_from_geom(camera_geometry)
    tensor_matrix = torch.tensor(np.ascontiguousarray(index_matrix.reshape(1, 1, *index_matrix.shape)))
    if camera_geometry.pix_type.value == "hexagon":
        camera_layout = "Hex"
    elif camera_geometry.pix_type.value == "square":
        camera_layout = "Square"
    else:
        raise ValueError("Unkown camera pixels type")
    return tensor_matrix, camera_layout


def get_dataset_geom(d, geometries):
    """
    Update `geometries` by append the geometries from d

    Parameters
    ----------
    d: list or `torch.utils.ConcatDataset` or `torch.utils.data.Subset` or `torch.utils.data.Dataset`
    geometries: list

    """
    if isinstance(d, list):
        for d_l in d:
            get_dataset_geom(d_l, geometries)
    else:
        geometries.append(fetch_dataset_geometry(d))


def inject_geometry_into_parameters(parameters: dict, camera_geometry):
    """
    Adds camera geometry in model backbone parameters

    Transformers models need the geometry to compute the positional embedding

    TODO: This is always called by the experiment runner, even if the model is not a transformer. Maybe it can be moved with other loading functions
    """
    for k, v in parameters.items():
        if k == "backbone":
            v["parameters"]["camera_geometry"] = camera_geometry
        elif isinstance(v, dict):
            parameters[k] = inject_geometry_into_parameters(v, camera_geometry)
    return parameters
