import os
import unittest

import torch
from ctapipe.instrument import CameraGeometry, SubarrayDescription

import gammalearn.data.image_processing.patchification
import gammalearn.nets.positional_embedding

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestTransformerUtils(unittest.TestCase):
    def test_patches_and_centroids_LSTCam(self):
        geom_LSTCam = CameraGeometry.from_name("LSTCam")
        patch_indices_LSTCam, patch_centroids_LSTCam = (
            gammalearn.data.image_processing.patchification.get_patch_indices_and_centroids_from_geometry(geom_LSTCam)
        )
        gammalearn.data.image_processing.patchification.check_patches(
            patch_indices_LSTCam, patch_centroids_LSTCam, geom_LSTCam
        )

    def test_patches_and_centroids_lstchain_07_MC(self):
        hdf5_file_path = os.path.join(THIS_DIR, "../../share/data/MC_data/dl1_gamma_example.h5")
        geometry = SubarrayDescription.from_hdf(hdf5_file_path).tel[1].camera.geometry
        patch_indices, patch_centroids = (
            gammalearn.data.image_processing.patchification.get_patch_indices_and_centroids_from_geometry(geometry)
        )
        gammalearn.data.image_processing.patchification.check_patches(patch_indices, patch_centroids, geometry)

    def test_patches_and_centroids_lstchain_07_real(self):
        hdf5_file_path = os.path.join(THIS_DIR, "../../share/data/real_data/dl1_realdata_example.h5")
        geometry = SubarrayDescription.from_hdf(hdf5_file_path).tel[1].camera.geometry
        patch_indices, patch_centroids = (
            gammalearn.data.image_processing.patchification.get_patch_indices_and_centroids_from_geometry(geometry)
        )
        gammalearn.data.image_processing.patchification.check_patches(patch_indices, patch_centroids, geometry)

    def test_2d_sincos_pos_embedding(self):
        geom_LSTCam = CameraGeometry.from_name("LSTCam")
        patch_indices_LSTCam, patch_centroids_LSTCam = (
            gammalearn.data.image_processing.patchification.get_patch_indices_and_centroids_from_geometry(geom_LSTCam)
        )
        pos_emb = gammalearn.nets.positional_embedding.get_2d_sincos_pos_embedding_from_patch_centroids(
            patch_centroids_LSTCam, 1024, ["class"]
        )
        assert pos_emb.shape == (266, 1024)
        assert torch.all(pos_emb[0] == 0)
        pos_emb = gammalearn.nets.positional_embedding.get_2d_sincos_pos_embedding_from_patch_centroids(
            patch_centroids_LSTCam, 1024, ["class", "energy"]
        )
        assert pos_emb.shape == (267, 1024)
        assert torch.all(pos_emb[1] == 1)
