import collections
import logging
import os
import unittest
import warnings

import numpy as np

from gammalearn.configuration.constants import ELECTRON_ID, GAMMA_ID, NAN_TIME_VALUE, PROTON_ID
from gammalearn.configuration.gl_logging import LOGGING_CONFIG
from gammalearn.data.dataset_event_filters.image_content_filters import intensity_filter
from gammalearn.data.LST_dataset import FileLSTDataset, MemoryLSTDataset

warnings.filterwarnings("ignore")

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

logging.config.dictConfig(LOGGING_CONFIG)


class TestLSTDataset(unittest.TestCase):
    def setUp(self) -> None:
        self.data_file = os.path.join(THIS_DIR, "../../share/data/MC_data/dl1_gamma_example.h5")
        self.camera_type = "LST_LSTCam"
        self.particle_dict = {GAMMA_ID: 1, ELECTRON_ID: 0, PROTON_ID: 0}
        self.subarray = [1]
        self.targets = collections.OrderedDict(
            {
                "energy": {
                    "output_shape": 1,
                },
                "impact": {
                    "output_shape": 2,
                },
                "direction": {
                    "output_shape": 2,
                },
                "class": {
                    "output_shape": 2,
                    "label_shape": 1,
                },
            }
        )
        self.group_by_image = {
            0: {
                "image_0": np.float32(0.45072153),
                "time_0": np.float32(20.453337),
                "labels": {
                    "energy": np.float32(2.4348483),
                    "corex": np.float32(-151.77223206),
                    "corey": np.float32(15.55177402),
                    "alt": np.float32(1.2186558),
                    "az": np.float32(3.151236),
                },
                "telescope": {
                    "alt": np.float32(1.2217305),
                    "az": np.float32(3.1415927),
                    "position": np.array([-6.336, 60.405, 12.5]),
                },
            },
            2: {
                "image_0": np.float32(-0.62957084),
                "time_0": np.float32(30.592175),
                "labels": {
                    "energy": np.float32(2.4348483),
                    "corex": np.float32(46.35375),
                    "corey": np.float32(195.51948547),
                    "alt": np.float32(1.2186558),
                    "az": np.float32(3.151236),
                },
                "telescope": {
                    "alt": np.float32(1.2217305),
                    "az": np.float32(3.1415927),
                    "position": np.array([-6.336, 60.405, 12.5]),
                },
            },
        }

        self.energy_filter_parameters = {
            "energy": [0.1, np.inf],
            "filter_only_gammas": True,
        }
        self.energy_filter_true_events = 25
        self.group_by_image_energy = {
            1: {
                "image_0": np.float32(0.7609045),
                "time_0": np.float32(6.604484),
            }
        }

        self.intensity_filter_parameters = {
            "intensity": [500, np.inf],
        }

        self.group_by_image_intensity = {
            1: {
                "image_0": np.float32(0.7609045),
                "time_0": np.float32(6.604484),
            }
        }

        self.intensity_lstchain_filter_parameters = {
            "intensity": [500, np.inf],
        }

        self.group_by_image_intensity_energy = {
            1: {
                "image_0": np.float32(0.7609045),
                "time_0": np.float32(6.604484),
            }
        }

        self.len_trig_energies = 25

    def test_mono_memory(self):
        dataset = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]
        assert np.isclose(
            sample_0["label"]["energy"],
            np.log10(self.group_by_image[0]["labels"]["energy"]),
        )
        assert np.isclose(
            sample_0["label"]["impact"][0],
            (self.group_by_image[0]["labels"]["corex"] - self.group_by_image[0]["telescope"]["position"][0]) / 1000,
        )
        assert np.isclose(
            sample_0["label"]["impact"][1],
            (self.group_by_image[0]["labels"]["corey"] - self.group_by_image[0]["telescope"]["position"][1]) / 1000,
        )
        assert np.isclose(
            sample_0["label"]["direction"][0],
            (self.group_by_image[0]["labels"]["alt"] - self.group_by_image[0]["telescope"]["alt"]),
        )
        assert np.isclose(
            sample_0["label"]["direction"][1],
            (self.group_by_image[0]["labels"]["az"] - self.group_by_image[0]["telescope"]["az"]),
        )

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]
        assert np.isclose(
            sample_2["label"]["energy"],
            np.log10(self.group_by_image[2]["labels"]["energy"]),
        )
        assert np.isclose(
            sample_2["label"]["impact"][0],
            (self.group_by_image[2]["labels"]["corex"] - self.group_by_image[2]["telescope"]["position"][0]) / 1000,
            rtol=5e-4,
        )
        assert np.isclose(
            sample_2["label"]["impact"][1],
            (self.group_by_image[2]["labels"]["corey"] - self.group_by_image[2]["telescope"]["position"][1]) / 1000,
        )

        assert np.isclose(
            sample_2["label"]["direction"][0],
            (self.group_by_image[2]["labels"]["alt"] - self.group_by_image[2]["telescope"]["alt"]),
        )
        assert np.isclose(
            sample_2["label"]["direction"][1],
            (self.group_by_image[2]["labels"]["az"] - self.group_by_image[2]["telescope"]["az"]),
        )

    def test_mono_memory_test_mode(self):
        dataset = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            train=False,
            subarray=self.subarray,
        )
        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]
        assert np.isclose(
            sample_0["dl1_params"]["mc_energy"],
            self.group_by_image[0]["labels"]["energy"],
        )
        assert np.isclose(
            sample_0["dl1_params"]["mc_core_x"],
            self.group_by_image[0]["labels"]["corex"] / 1000,
        )
        assert np.isclose(sample_0["dl1_params"]["mc_alt"], self.group_by_image[0]["labels"]["alt"])

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]
        assert np.isclose(
            sample_2["dl1_params"]["mc_energy"],
            self.group_by_image[2]["labels"]["energy"],
        )
        assert np.isclose(
            sample_2["dl1_params"]["mc_core_x"],
            self.group_by_image[2]["labels"]["corex"] / 1000,
            rtol=5e-4,
        )
        assert np.isclose(sample_2["dl1_params"]["mc_alt"], self.group_by_image[2]["labels"]["alt"])

    def test_mono_file(self):
        dataset = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )

        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]
        assert np.isclose(
            sample_0["label"]["energy"],
            np.log10(self.group_by_image[0]["labels"]["energy"]),
        )
        assert np.isclose(
            sample_0["label"]["impact"][0],
            (self.group_by_image[0]["labels"]["corex"] - self.group_by_image[0]["telescope"]["position"][0]) / 1000,
        )
        assert np.isclose(
            sample_0["label"]["impact"][1],
            (self.group_by_image[0]["labels"]["corey"] - self.group_by_image[0]["telescope"]["position"][1]) / 1000,
        )
        assert np.isclose(
            sample_0["label"]["direction"][0],
            (self.group_by_image[0]["labels"]["alt"] - self.group_by_image[0]["telescope"]["alt"]),
        )
        assert np.isclose(
            sample_0["label"]["direction"][1],
            (self.group_by_image[0]["labels"]["az"] - self.group_by_image[0]["telescope"]["az"]),
        )

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]
        assert np.isclose(
            sample_2["label"]["energy"],
            np.log10(self.group_by_image[2]["labels"]["energy"]),
        )
        assert np.isclose(
            sample_2["label"]["impact"][0],
            (self.group_by_image[2]["labels"]["corex"] - self.group_by_image[2]["telescope"]["position"][0]) / 1000,
            rtol=5e-4,
        )
        assert np.isclose(
            sample_2["label"]["impact"][1],
            (self.group_by_image[2]["labels"]["corey"] - self.group_by_image[2]["telescope"]["position"][1]) / 1000,
        )

        assert np.isclose(
            sample_2["label"]["direction"][0],
            (self.group_by_image[2]["labels"]["alt"] - self.group_by_image[2]["telescope"]["alt"]),
        )
        assert np.isclose(
            sample_2["label"]["direction"][1],
            (self.group_by_image[2]["labels"]["az"] - self.group_by_image[2]["telescope"]["az"]),
        )

    def test_energy_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_event({})
        assert len(dataset_mono.dl1_params["mc_energy"]) == self.energy_filter_true_events

        sample_1 = dataset_mono[1]

        assert sample_1["image"][0, 0] == self.group_by_image_energy[1]["image_0"]
        assert sample_1["image"][1, 0] == self.group_by_image_energy[1]["time_0"]

    def test_energy_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_event({})
        assert len(dataset_mono.dl1_params["mc_energy"]) == self.energy_filter_true_events

        sample_1 = dataset_mono[1]

        assert sample_1["image"][0, 0] == self.group_by_image_energy[1]["image_0"]
        assert sample_1["image"][1, 0] == self.group_by_image_energy[1]["time_0"]

    def test_intensity_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        sample_0 = dataset_mono[1]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[1]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[1]["time_0"]

    def test_intensity_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        sample_0 = dataset_mono[1]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[1]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[1]["time_0"]

    def test_intensity_lstchain_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_lstchain_filter_parameters})
        sample_0 = dataset_mono[1]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[1]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[1]["time_0"]

    def test_intensity_lstchain_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_lstchain_filter_parameters})
        sample_0 = dataset_mono[1]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[1]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[1]["time_0"]

    def test_intensity_energy_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        dataset_mono.filter_event({})

        sample_2 = dataset_mono[1]
        assert sample_2["image"][0, 0] == self.group_by_image_intensity_energy[1]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image_intensity_energy[1]["time_0"]

    def test_intensity_energy_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        dataset_mono.filter_event({})

        sample_2 = dataset_mono[1]
        assert sample_2["image"][0, 0] == self.group_by_image_intensity_energy[1]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image_intensity_energy[1]["time_0"]

    def test_subarray(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        assert len(dataset_mono.trig_energies) == self.len_trig_energies
        assert len(dataset_mono.images) == self.len_trig_energies

    # TODO test stereo
    def test_mask_channel(self):
        """
        Test mask_channel() module.
        Creation of a 2x2 np.ndarray for time and image.
        Checking if the function returns an image and a time with 0 when mask pixel is set to False
        and unchanged pixel value when mask pixel is set to True.
        """
        input_image = np.array([[1, 2], [3, 4]], dtype=np.float32)
        input_time = np.array([[3, 5], [7, 11]], dtype=np.float32)
        input_mask = np.array([[False, True], [True, False]], dtype=np.bool_)
        expected_image = np.array([[0, 2], [3, 0]], dtype=np.float32)
        expected_time = np.array([[NAN_TIME_VALUE, 5], [7, NAN_TIME_VALUE]], dtype=np.float32)

        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
            mask_method="precomputed_lstchain",
        )

        dataset_mono.images = input_image
        dataset_mono.times = input_time
        dataset_mono.mask_channel(input_mask)

        np.testing.assert_equal(expected_image, dataset_mono.images)  # Test mask on image
        np.testing.assert_equal(expected_time, dataset_mono.times)  # Test mask on time

    def test_compute_tailcuts_cleaning_masks(self):
        """
        Test compute_tailcuts_cleaning_masks()

        Checks that :
        - adding cleaning_mask is not removing all images.
        - adding cleaning_mask is not adding more images than without cleaning_mask.
        - images have shape [2x?]
        - mask_method is set to tailcuts_standard_analysis
        - applying mask should lower the quantity of signal on the images.

        """

        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
            mask_method="tailcuts_standard_analysis",
        )

        dataset_no_mask = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        assert dataset_mono.mask_method == "tailcuts_standard_analysis"
        assert len(dataset_mono.images) > 0
        assert len(dataset_mono.images) <= len(dataset_no_mask.images)
        assert dataset_mono[0]["image"].shape[0] == 2
        assert len(dataset_mono.images_masks) == len(dataset_mono.images)
        assert np.sum(dataset_mono.images) <= np.sum(dataset_no_mask.images)

    def test_compute_data_reduction_masks(self):
        """
        Test compute_data_reduction_masks()

        Checks that :
        - adding cleaning_mask is not removing all images.
        - adding cleaning_mask is not adding more images than without cleaning_mask.
        - images have shape [2x?]
        - mask_method is set to data_reduction_mask
        - applying mask should lower the quantity of signal on the images.

        """

        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
            mask_method="data_reduction_mask",
        )

        dataset_no_mask = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            self.targets,
            self.particle_dict,
            use_time=True,
            subarray=self.subarray,
        )
        assert dataset_mono.mask_method == "data_reduction_mask"
        assert len(dataset_mono.images) > 0
        assert len(dataset_mono.images) <= len(dataset_no_mask.images)
        assert dataset_mono[0]["image"].shape[0] == 2
        assert len(dataset_mono.images_masks) == len(dataset_mono.images)
        assert len(dataset_mono.images_masks) == len(dataset_mono.times)
        assert np.sum(dataset_mono.images) <= np.sum(dataset_no_mask.images)

    def test_wrong_mask_method(self):
        """
        Check that MemoryLSTDataset raises ValueError if an unknown mask method is used.
        """
        with self.assertRaises(ValueError):
            MemoryLSTDataset(
                self.data_file,
                self.camera_type,
                "image",
                self.targets,
                self.particle_dict,
                use_time=True,
                subarray=self.subarray,
                mask_method="unknown_method_1234",
            )


class TestLSTRealDataset(unittest.TestCase):
    def setUp(self) -> None:
        self.data_file = os.path.join(THIS_DIR, "../../share/data/real_data/dl1_realdata_example.h5")
        self.camera_type = "LST_LSTCam"
        self.subarray = [1]
        self.group_by_image = {
            0: {
                "image_0": np.float32(40.915554),
                "time_0": np.float32(14.287617),
                "telescope": {
                    "alt": np.float32(1.25764907),
                    "az": np.float32(0.80768447),
                    "position": np.array([50.0, 50.0, 16.0]),
                },
            },
            2: {
                "image_0": np.float32(13.920349),
                "time_0": np.float32(17.394579),
                "telescope": {
                    "alt": np.float32(1.25764908),
                    "az": np.float32(0.80768444),
                    "position": np.array([50.0, 50.0, 16.0]),
                },
            },
        }

        self.intensity_filter_parameters = {
            "intensity": [
                0,
                250 + 20 * 1855,
            ],  # new test files have added noise 20 * np.random.rand()
        }

        self.group_by_image_intensity = {
            0: {
                "image_0": np.float32(40.915554),
                "time_0": np.float32(14.287617),
            }
        }

        self.intensity_lstchain_filter_parameters = {
            "intensity": [0, 250 + 20 * 1855],
        }  # threshold must match intensity_filter_parameters

    def test_mono_memory(self):
        dataset = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        assert dataset.trig_energies is None

        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]

    def test_mono_memory_test_mode(self):
        dataset = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            train=False,
            subarray=self.subarray,
        )
        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]

    def test_mono_file(self):
        dataset = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        sample_0 = dataset[0]
        assert sample_0["image"][0, 0] == self.group_by_image[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image[0]["time_0"]

        sample_2 = dataset[2]

        assert sample_2["image"][0, 0] == self.group_by_image[2]["image_0"]
        assert sample_2["image"][1, 0] == self.group_by_image[2]["time_0"]

    def test_intensity_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        sample_0 = dataset_mono[0]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[0]["time_0"]

    def test_intensity_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_filter_parameters})
        sample_0 = dataset_mono[0]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[0]["time_0"]

    def test_intensity_lstchain_filter_memory(self):
        dataset_mono = MemoryLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_lstchain_filter_parameters})
        sample_0 = dataset_mono[0]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[0]["time_0"]

    def test_intensity_lstchain_filter_file(self):
        dataset_mono = FileLSTDataset(
            self.data_file,
            self.camera_type,
            "image",
            use_time=True,
            subarray=self.subarray,
        )
        dataset_mono.filter_image({intensity_filter: self.intensity_lstchain_filter_parameters})
        sample_0 = dataset_mono[0]
        assert sample_0["image"][0, 0] == self.group_by_image_intensity[0]["image_0"]
        assert sample_0["image"][1, 0] == self.group_by_image_intensity[0]["time_0"]

    # TODO test stereo


class TestDL1Parameters(unittest.TestCase):
    def setUp(self) -> None:
        self.lst1_file = os.path.join(THIS_DIR, "../../share/data/real_data/dl1_realdata_example.h5")
        self.mc_file = os.path.join(THIS_DIR, "../../share/data/MC_data/dl1_gamma_example.h5")
        self.camera_type = "LST_LSTCam"
        self.group_by = "image"
        self.targets = []
        self.particle_dict = {GAMMA_ID: 1, PROTON_ID: 0}

    def test_train_dl1_parameters(self):
        mc_dataset = MemoryLSTDataset(
            self.mc_file,
            camera_type=self.camera_type,
            group_by=self.group_by,
            targets=self.targets,
            particle_dict=self.particle_dict,
        )
        lst1_dataset = MemoryLSTDataset(
            self.lst1_file,
            camera_type=self.camera_type,
            group_by=self.group_by,
            targets=self.targets,
            particle_dict=self.particle_dict,
        )
        # "ucts_jump" new key in lst1_dataset but not in mc_dataset so can't compare all keys to all keys
        assert all([k in lst1_dataset[0]["dl1_params"].keys() for k in mc_dataset[0]["dl1_params"].keys()])
        # assert mc_dataset[0]['dl1_params'].keys() == lst1_dataset[0]['dl1_params'].keys()

    def test_test_dl1_parameters(self):
        mc_dataset = MemoryLSTDataset(
            self.mc_file,
            camera_type=self.camera_type,
            group_by=self.group_by,
            targets=self.targets,
            particle_dict=self.particle_dict,
            train=False,
        )
        lst1_dataset = MemoryLSTDataset(
            self.lst1_file,
            camera_type=self.camera_type,
            group_by=self.group_by,
            targets=self.targets,
            particle_dict=self.particle_dict,
            train=False,
        )
        assert list(mc_dataset[0]["dl1_params"].keys()) == mc_dataset.dl1_param_names
        assert list(lst1_dataset[0]["dl1_params"].keys()) == lst1_dataset.dl1_param_names


if __name__ == "__main__":
    unittest.main()
