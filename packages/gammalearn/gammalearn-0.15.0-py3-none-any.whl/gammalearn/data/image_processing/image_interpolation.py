# TODO: Should we implement transform using pytorch transform base class and __forward__
#                                   or using a python class and __call__


import numpy as np
from astropy import units as u
from dl1_data_handler.image_mapper import ImageMapper


class TransformIACT:
    """Base class for all transforms that require the camera geometry (see BaseLSTDataset __init__  where transform set-up is done)"""

    def setup_geometry(self, camera_geometry):
        raise NotImplementedError


class ResampleImage(TransformIACT):
    """
    Resample an hexagonal image with DL1 Data Handler Image Mapper
    The class needs to be instantiated first to be passed to a Dataset class but can be setup later when the camera
    information is available to the user
    """

    def __init__(self, mapping, output_size):
        self.camera = None
        self.image_mapper = None
        self.mapping = mapping
        self.output_size = output_size

    def setup_geometry(self, camera_geometry):
        # We need to rotate the camera for ImageMapper
        camera_geometry.rotate(camera_geometry.pix_rotation)
        pix_pos = np.array(
            [
                camera_geometry.pix_x.to_value(u.m),
                camera_geometry.pix_y.to_value(u.m),
            ]
        )
        self.camera = camera_geometry.name
        self._setup_image_mapper(pix_pos)

    def _setup_image_mapper(self, pix_pos):
        self.image_mapper = ImageMapper(
            pixel_positions={self.camera: pix_pos},
            camera_types=[self.camera],
            mapping_method={self.camera: self.mapping},
            interpolation_image_shape={self.camera: self.output_size},
        )

    def __call__(self, data):
        mapped_data = self.image_mapper.map_image(data.T, self.camera)
        return mapped_data.T
