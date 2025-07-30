import unittest

import numpy as np
from ctapipe.instrument import CameraGeometry

import gammalearn.data.image_processing.data_volume_reduction as dvr


class DataVolumeReductionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.charge_map = np.array(
            [[0, 0, 1, 0, 0], [0, 4, 4, 4, 0], [1, 4, 10, 4, 1], [0, 4, 4, 4, 0], [0, 0, 1, 0, 0]], dtype=np.float32
        )
        self.min_charge_for_certain_selection = 8
        # create a charge with only one pixel above the threshold
        self.charge_map_full_event_test = (self.min_charge_for_certain_selection + 1) * np.ones(
            (5, 5), dtype=np.float32
        )
        self.charge_map_full_event_test[0, 0] = 0
        self.number_dilations = 1
        self.camera_geometry = CameraGeometry.from_name("LSTCam")
        # mock for camera_geometry.neighbor_matrix
        self.camera_geometry = self.camera_geometry.make_rectangular(5, 5)
        self.min_npixels_for_full_event = 20

        self.selected_pixels = np.array(
            [
                [False, False, False, False, False],
                [False, False, True, False, False],
                [False, True, True, True, False],
                [False, False, True, False, False],
                [False, False, False, False, False],
            ],
            dtype=np.bool_,
        )

        self.full_mask = np.ones((5, 5), dtype=np.bool_)

    def test_get_selected_pixels(self) -> None:
        """Test if binary mask is correctly compute and dilate once on a rectangular image."""
        selected_pixels = dvr.get_selected_pixels(
            self.charge_map.flatten(),
            self.min_charge_for_certain_selection,
            self.number_dilations,
            self.camera_geometry,
            self.min_npixels_for_full_event,
        )
        self.assertTrue(np.array_equal(self.selected_pixels.flatten(), selected_pixels))

    def test_get_selected_pixels_full_event(self) -> None:
        """Test when the sum of the selected_pixels is above the min_npixels_for_full_event, the full event is return (not the slected mask)."""
        selected_pixels = dvr.get_selected_pixels(
            self.charge_map_full_event_test.flatten(),
            self.min_charge_for_certain_selection,
            self.number_dilations,
            self.camera_geometry,
            self.min_npixels_for_full_event,
        )
        self.assertTrue(np.array_equal(self.full_mask.flatten(), selected_pixels))
