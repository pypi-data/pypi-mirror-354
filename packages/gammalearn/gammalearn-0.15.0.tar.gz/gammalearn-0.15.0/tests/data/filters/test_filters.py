import unittest

import numpy as np
import torch
from ctapipe.instrument import CameraGeometry

import gammalearn.data.telescope_geometry


class MockLSTDataset(object):
    def __init__(self):
        self.images = np.array([np.full(1855, 0.001), np.full(1855, 1), np.full(1855, 0.0001), np.full(1855, 0.1)])
        self.images[3, 903:910] = 30
        self.images[2, 1799:1806] = 10  # for cleaning and leakage
        self.camera_type = "LST_LSTCam"
        self.group_by = "image"
        self.original_geometry = CameraGeometry.from_name("LSTCam")
        self.simu = True
        self.dl1_params = {
            "event_id": np.array([0, 0, 1, 2]),
            "mc_type": np.array([1, 0, 0, 0]),
            "mc_energy": np.array([0.010, 2.5, 0.12, 0.8]),
            "log_mc_energy": np.log10(np.array([0.010, 2.5, 0.12, 0.8])),
            "mc_alt_tel": np.full(4, np.deg2rad(70)),
            "mc_az_tel": np.full(4, np.deg2rad(180)),
            "mc_alt": np.deg2rad([71, 75, 68, 69]),
            "mc_az": np.deg2rad([180, 180, 179.5, 175]),
            "mc_core_x": np.array([50.3, -150, -100, 100]) / 1000,
            "mc_core_y": np.array([48, -51, 0, 0]) / 1000,
            "tel_id": np.array([2, 1, 3, 1]),
            "tel_pos_x": np.array([75.28, -70.93, -70.93, -70.93]) / 1000,
            "tel_pos_y": np.array([50.46, -52.07, 53.1, -52.07]) / 1000,
        }

    def __len__(self):
        return len(self.images)


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaning_true_mask = [False, False, True, True]

        self.energy_parameters = {"energy": [0.02, 2], "filter_only_gammas": True}
        self.energy_true_mask = [True, False, True, True]

        self.net_parameters_dic = {
            "model": "GammaPhysNet",
            "parameters": {
                "backbone": {
                    "model": "ResNetAttentionIndexed",
                    "parameters": {
                        "num_layers": 3,
                        "initialization": (torch.nn.init.kaiming_uniform_, {"mode": "fan_out"}),
                        "normalization": (torch.nn.BatchNorm2d, {}),
                        "num_channels": 2,
                        "block_features": [16, 32, 64],
                        "attention_layer": ("DualAttention", {"ratio": 16}),
                    },
                },
                "fc_width": 256,
                "last_bias_init": None,
            },
        }

    def test_inject_geometry_into_parameters(self):
        self.net_parameters_dic = gammalearn.data.telescope_geometry.inject_geometry_into_parameters(
            self.net_parameters_dic, "LSTCam_geometry"
        )
        assert self.net_parameters_dic["parameters"]["backbone"]["parameters"]["camera_geometry"] == "LSTCam_geometry"
