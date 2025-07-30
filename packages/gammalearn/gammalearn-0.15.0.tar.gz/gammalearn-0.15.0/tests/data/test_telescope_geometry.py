import unittest
from copy import deepcopy

import astropy.units as u
import numpy as np
from ctapipe.instrument import CameraGeometry

import gammalearn.data.telescope_geometry


class TestIndexMatrix(unittest.TestCase):
    def setUp(self):
        lstcam_geom = CameraGeometry.from_name("LSTCam")
        self.minihex = deepcopy(lstcam_geom)
        self.minihex.camera_name = "minihex"

    def test_get_index_matrix_from_geom_7(self):
        """
        Test the converter with a simple 7 pixels geometry

        Hexa:
        ```
          0   1

        2   3   4

          5   6
        ```
        Square:
        ```
         0   1  -1
         2   3   4
        -1   5   6
        ```
        """
        minihex = self.minihex
        # make a test geometry with 7 pixels
        minihex.n_pixels = 7
        short_dist = np.sqrt(3) / 2
        minihex.pix_x = 0.05 * np.array([-0.5, 0.5, -1, 0, 1, -0.5, 0.5]) * u.m
        minihex.pix_y = 0.05 * np.array([short_dist, short_dist, 0, 0, 0, -short_dist, -short_dist]) * u.m
        minihex.pix_rotation *= 0
        minihex.neighbors = minihex.neighbors[:7]
        minihex.pix_id = minihex.pix_id[:7]
        minihex.pixel_width = minihex.pixel_width[:7]

        # fix the neighbors
        minihex.neighbors = [[1, 2, 3], [0, 3, 4], [0, 3, 5], [0, 1, 2, 4, 5, 6], [1, 3, 6], [2, 3, 6], [4, 3, 5]]

        idx_mat = gammalearn.data.telescope_geometry.get_index_matrix_from_geom(minihex)

        np.testing.assert_array_equal(idx_mat, [[0, 1, -1], [2, 3, 4], [-1, 5, 6]])

    def test_get_index_matrix_from_geom_19(self):
        """
        Test the converter with a simple 19 pixels geometry

        Hexa:
        ```

             0   1   2

           3   4   5   6

          7  8   9  10  11

            12 13  14  15

              16 17 18
        ```
        Square:
        ```
         0   1   2  -1  -1

         3   4   5   6  -1

         7   8   9  10  11

        -1  12  13  14  15

        -1  -1  16  17  18
        ```
        """
        minihex = self.minihex

        minihex.n_pixels = 19
        short_dist = np.sqrt(3) / 2
        minihex.pix_x = (
            0.05
            * np.array(
                [
                    -1,
                    0,
                    1,
                    -1.5,
                    -0.5,
                    0.5,
                    1.5,
                    -2,
                    -1,
                    0,
                    1,
                    2,
                    -1.5,
                    -0.5,
                    0.5,
                    1.5,
                    -1,
                    0,
                    1,
                ]
            )
            * u.m
        )

        minihex.pix_y = (
            0.05
            * np.array(
                [
                    2 * short_dist,
                    2 * short_dist,
                    2 * short_dist,
                    short_dist,
                    short_dist,
                    short_dist,
                    short_dist,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -short_dist,
                    -short_dist,
                    -short_dist,
                    -short_dist,
                    -2 * short_dist,
                    -2 * short_dist,
                    -2 * short_dist,
                ]
            )
            * u.m
        )

        minihex.pix_rotation *= 0

        minihex.neighbors = minihex.neighbors[: minihex.n_pixels]
        minihex.pix_id = minihex.pix_id[: minihex.n_pixels]
        minihex.pixel_width = minihex.pixel_width[: minihex.n_pixels]

        # fix the neighbors
        minihex.neighbors = [
            [1, 3, 4],
            [0, 4, 5, 2],
            [1, 5, 6],
            [0, 4, 7, 8],
            [0, 1, 5, 9, 8, 3],
            [1, 2, 6, 10, 9, 4],
            [2, 5, 10, 11],
            [7, 8, 12],
            [3, 4, 9, 13, 12, 7],
            [4, 5, 10, 14, 13, 8],
            [5, 6, 11, 15, 14, 9],
            [6, 10, 15],
            [7, 8, 13, 16],
            [8, 9, 14, 17, 16, 12],
            [9, 10, 15, 18, 17, 13],
            [10, 11, 14, 18],
            [12, 13, 17],
            [13, 14, 16, 18],
            [14, 15, 17],
        ]

        idx_mat = gammalearn.data.telescope_geometry.get_index_matrix_from_geom(minihex)

        np.testing.assert_array_equal(
            idx_mat,
            [[0, 1, 2, -1, -1], [3, 4, 5, 6, -1], [7, 8, 9, 10, 11], [-1, 12, 13, 14, 15], [-1, -1, 16, 17, 18]],
        )
