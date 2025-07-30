import numpy as np
from ctapipe.instrument import CameraGeometry
from torch.utils.data import Dataset


class MockLSTDataset(Dataset):
    def __init__(
        self,
        hdf5_file_path,
        camera_type,
        group_by,
        targets=None,
        particle_dict=None,
        use_time=False,
        train=True,
        subarray=None,
        transform=None,
        target_transform=None,
        **kwargs,
    ):
        self.images = np.random.rand(50, 1855).astype(np.float32)
        self.times = np.random.rand(50, 1855).astype(np.float32)

        self.particle_dict = {0: 0, 101: 1}

        self.camera_type = "LST_LSTCam"
        self.group_by = "image"
        self.original_geometry = CameraGeometry.from_name("LSTCam")
        self.camera_geometry = CameraGeometry.from_name("LSTCam")
        self.simu = True
        self.dl1_params = {
            "event_id": np.arange(50),
            "mc_type": np.random.choice([101, 0], size=50),
            "mc_energy": np.random.rand(50).astype(np.float32),
            "log_mc_energy": np.random.rand(50).astype(np.float32),
            "mc_alt_tel": np.full(50, np.deg2rad(70), dtype=np.float32),
            "mc_az_tel": np.full(50, np.deg2rad(180), dtype=np.float32),
            "mc_alt": np.random.rand(50).astype(np.float32),
            "mc_az": np.random.rand(50).astype(np.float32),
            "mc_core_x": np.random.rand(50).astype(np.float32),
            "mc_core_y": np.random.rand(50).astype(np.float32),
            "tel_id": np.random.rand(50).astype(np.float32),
            "tel_pos_x": np.random.rand(50).astype(np.float32),
            "tel_pos_y": np.random.rand(50).astype(np.float32),
        }

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        data = np.stack([self.images[idx], self.times[idx]])
        dl1_params = {n: p[idx] for n, p in self.dl1_params.items()}
        labels = {
            "energy": np.array([dl1_params["log_mc_energy"]], dtype=np.float32),
            "impact": np.array(
                [
                    dl1_params["mc_core_x"] - dl1_params["tel_pos_x"],
                    dl1_params["mc_core_y"] - dl1_params["tel_pos_y"],
                ],
                dtype=np.float32,
            ),
            "direction": np.array(
                [
                    dl1_params["mc_alt"] - dl1_params["mc_alt_tel"],
                    dl1_params["mc_az"] - dl1_params["mc_az_tel"],
                ],
                dtype=np.float32,
            ),
            "class": self.particle_dict.get(dl1_params["mc_type"], -1),
        }
        sample = {"image": data, "dl1_params": dl1_params, "label": labels}

        return sample

    def filter_image(self, filter_dict):
        pass

    def filter_event(self, filter_dict):
        pass
