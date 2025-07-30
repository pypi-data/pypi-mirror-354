import numpy as np
import pandas as pd
import tables
import torch
from ctapipe.image import tailcuts_clean
from ctapipe.instrument import CameraGeometry, SubarrayDescription
from lstchain.io.io import dl1_images_lstcam_key, dl1_params_lstcam_key, read_simu_info_merged_hdf5
from torch.utils.data import Dataset

import gammalearn.data.image_processing.data_volume_reduction as dvr
from gammalearn.configuration.constants import NAN_TIME_VALUE, REAL_DATA_ID, SOURCE, TARGET
from gammalearn.data.telescope_geometry import WrongGeometryError
from gammalearn.data.transforms import GLearnCompose

DL1_SUBARRAY_TRIGGER_KEY = "dl1/event/subarray/trigger"
DL1_SUBARRAY_LAYOUT = "configuration/instrument/subarray/layout"
KNOWN_MASK_METHODS = [
    "tailcuts_standard_analysis",
    "precomputed_lstchain",
    "data_reduction_mask",
]


class BaseLSTDataset(Dataset):
    """Camera dataset for lstchain DL1 hdf5 files. Tested with lstchain 0.7.
    Handles a single file at the time.

    Implements the logic of the batch of data and paths to load from file. The actual data loading, at initialization
    or during dataset iteration is implemented in children classes.

    """

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
        domain_dict=None,
        domain=None,
        **kwargs,
    ):
        """
        Parameters
        ----------
            hdf5_file_path (str): path to hdf5 file containing the data
            camera_type (str) : name of the camera used (e.g. camera_type='LST_LSTCam')
            group_by (str): the way to group images in the dataset (e.g. 'event_triggered_tels' :
            by event only for telescopes which triggered)
            targets (list, optional): the targets to include in the sample
            particle_dict (dict, optional): Dictionary of particle types
            use_time (bool, optional): whether or not include the time peak in the sample
            train (bool, optional): defines the dataset mode (train or test)
            subarray (Array, optional): array of telescopes ids that defines the subarray used
            transform (callable, optional): Optional transform to be applied on a sample
            target_transform (callable, optional): Optional transform to be applied on a sample
        """
        self.hdf5_file_path = hdf5_file_path
        self.hdf5_file = None
        self.camera_type = camera_type
        if not self.camera_type == "LST_LSTCam":
            WrongGeometryError("passed camera_type should be LST_LSTCam")

        self.targets = targets if targets is not None else {}
        self.particle_dict = particle_dict
        self.transform = transform
        self.target_transform = target_transform
        self.use_time = use_time
        self.train = train

        self.images = None
        self.pedestals = None
        self.times = None
        self.filtered_indices = None
        self.lstchain_version = None
        self.simu = True
        self.domain = "source" if domain is None else domain
        self.domain_dict = domain_dict

        self.mc_only_dl1_parameters = [
            "disp_angle",
            "disp_dx",
            "disp_dy",
            "disp_norm",
            "disp_sign",
            "log_mc_energy",
            "src_x",
            "src_y",
        ]
        self.lst1_only_dl1_parameters = (
            "dragon_time",
            "tib_time",
            "ucts_time",
            "ucts_trigger_type",
        )

        group_by_options = ["image", "event_all_tels", "event_triggered_tels"]

        assert group_by in group_by_options, "{} is not a suitable group option. Must be in {}".format(
            group_by, group_by_options
        )

        self.group_by = group_by

        # LSTCam is used as default geometry at the moment.
        # all data (MC and real) are converted to this geom.
        self.camera_geometry = CameraGeometry.from_name("LSTCam")

        # Note: when using ctapipe>=0.12, the following code might be used:
        self.original_geometry = SubarrayDescription.from_hdf(hdf5_file_path).tel[1].camera.geometry

        # Rotate the original geometry as well to align both geometries
        # self.original_geometry.rotate(self.original_geometry.pix_rotation)

        self.inj_table = self.original_geometry.position_to_pix_index(
            self.camera_geometry.pix_x, self.camera_geometry.pix_y
        )

        # Load simu info if available
        try:
            self.run_config = {"mcheader": read_simu_info_merged_hdf5(self.hdf5_file_path)}
        except IndexError:
            self.simu = False
            self.run_config = {}
        if self.simu:
            assert particle_dict is not None, "You must define a particle dictionary for MC dataset !"
        self.targets = {} if self.targets is None else self.targets
        self.run_config["metadata"] = {}

        with tables.File(hdf5_file_path, "r") as hdf5_file:
            for attr in hdf5_file.root._v_attrs._f_list("user"):
                self.run_config["metadata"][attr] = hdf5_file.root._v_attrs[attr]

            # We load parameters as they can be used to filter events.
            self.dl1_params = hdf5_file.root[dl1_params_lstcam_key][:]
            self.dl1_param_names = hdf5_file.root[dl1_params_lstcam_key].colnames

            # Update MC only dl1 parameters with all parameters starting with "mc_"
            self.mc_only_dl1_parameters.extend(
                [col for col in self.dl1_param_names if "mc_" in col and col != "mc_type"]
            )

            # image related infos
            self.filtered_indices = np.arange(len(hdf5_file.root[dl1_images_lstcam_key]), dtype=int)

            # LST subarray
            layout = hdf5_file.root[DL1_SUBARRAY_LAYOUT][:]
            lst_layout_mask = layout["name"] == b"LST"
            self.layout_tel_ids = layout["tel_id"][lst_layout_mask]

            if self.simu:
                dl1_params_df = pd.DataFrame(
                    {
                        "obs_id": self.dl1_params["obs_id"],
                        "event_id": self.dl1_params["event_id"],
                    }
                )
                dl1_params_df = dl1_params_df.set_index(["obs_id", "event_id"])
                unique_event_mask = ~dl1_params_df.index.duplicated(keep="first")
                self.trig_energies = self.dl1_params["mc_energy"][unique_event_mask]
                self.trig_tels = hdf5_file.root[DL1_SUBARRAY_TRIGGER_KEY][:]["tels_with_trigger"]
            else:
                self.trig_energies = None
                self.trig_tels = np.full((len(self.dl1_params), 6), False)
                self.trig_tels[:, np.searchsorted(layout["tel_id"], self.dl1_params["tel_id"])] = (
                    True  # TODO fix when real data has several tels
                )

                # Get the pedestal id. Used by GPN-CBN in inference to compute the first order statistic of the NSB
                # using the pedestals.
                params = hdf5_file.root[dl1_params_lstcam_key][:]
                images = hdf5_file.root[dl1_images_lstcam_key][:]
                pedestals_id = params[params["event_type"] == 2]["event_id"]
                # Filter the images based on the event id and keep the pedestal images only
                images_id = np.in1d(images["event_id"], pedestals_id)
                self.pedestals = images[images_id]["image"]

            # Select sub-subarray, select events from a defined subarray (e.g. only LST1)
            if subarray is not None:
                assert np.in1d(subarray, self.layout_tel_ids).all(), "All the telescopes of the subarray must be LSTs"
                self.layout_tel_ids = subarray
            subarray_mask = np.any(
                self.trig_tels[:, np.searchsorted(layout["tel_id"], self.layout_tel_ids)],
                axis=1,
            )
            if self.trig_energies is not None:
                self.trig_energies = self.trig_energies[subarray_mask]
            event_mask = np.in1d(self.dl1_params["tel_id"], self.layout_tel_ids)
            self.dl1_params = self.dl1_params[event_mask]
            self.filtered_indices = self.filtered_indices[event_mask]

            # Load event info, when multiple telescopes are used, event id can be duplicated (multiple trigger for the same event)
            self.unique_event_ids = np.unique(self.dl1_params[:]["event_id"])

            # If we mix simu and real data (e.g. auto-encoding using both domains), we need dict keys to be the same
            # We use -9999 as a default label for real data
            if not self.simu and "mc_type" not in self.dl1_params.dtype.names:
                self.dl1_params["mc_type"] = np.full(len(self.dl1_params), -9999)

            if self.simu:
                # Turn distances into km (sort of normalisation)
                self.dl1_params["mc_x_max"] /= 1000
                self.dl1_params["mc_core_x"] /= 1000
                self.dl1_params["mc_core_y"] /= 1000
            self.dl1_params["tel_pos_x"] /= 1000
            self.dl1_params["tel_pos_y"] /= 1000
            self.dl1_params["tel_pos_z"] /= 1000

        # setup the ImageMapper transform, for special Transforms that required some info loaded with the dataset
        if self.transform is not None:
            if hasattr(self.transform, "setup_geometry"):
                self.transform.setup_geometry(self.camera_geometry)
            elif hasattr(self.transform, "transforms"):
                for t in self.transform.transforms:
                    if hasattr(t, "setup_geometry"):
                        t.setup_geometry(self.camera_geometry)

    def __len__(self):
        if self.group_by == "image":
            return len(self.filtered_indices)
        else:
            return len(self.unique_event_ids)

    def _get_sample(self, idx):
        if self.group_by == "image":
            data_t = self._get_image_data(idx)
            data = np.stack(data_t) if self.use_time else data_t[0]
            dl1_params = self.dl1_params[idx]
        else:
            event_id = self.unique_event_ids[idx]
            filtered_images_ids = np.arange(len(self.dl1_params))[self.dl1_params["event_id"] == event_id]
            dl1_params = self.dl1_params[self.dl1_params["event_id"] == event_id]
            tel_ids = dl1_params["tel_id"] - 1  # telescope ids start from 1
            dl1_params = dl1_params[0] if dl1_params.ndim > 1 else dl1_params
            if self.group_by == "event_all_tels":
                # We want as many images as telescopes
                images_ids = np.full(len(self.layout_tel_ids), -1)
                images_ids[tel_ids] = filtered_images_ids
            elif self.group_by == "event_triggered_tels":
                images_ids = filtered_images_ids
            else:
                raise ValueError("group_by option has an incorrect value.")
            data_t = self._get_image_data(images_ids)
            if self.use_time:
                assert len(data_t) == 2, "When using both charge and peakpos you need the same" "amount of each"
                event_images = data_t[0]
                event_times = data_t[1]
                event_images = np.nan_to_num(event_images)
                event_times = np.nan_to_num(event_times, nan=NAN_TIME_VALUE)

                data = np.empty((event_images.shape[0] * 2, event_images.shape[1]), dtype=np.float32)
                data[0::2, :] = event_images
                data[1::2, :] = event_times
            else:
                data = data_t[0]

        # We reogranize the pixels to match the 'LSTCam' geometry
        sample = {"image": data[..., self.inj_table]}
        transform_params = {}
        if self.transform:
            if isinstance(self.transform, GLearnCompose):
                # Some Transforms need extra parameters
                # TODO: check how lightning does Transform using forward, instead of class with __call__
                sample["image"], transform_params = self.transform(
                    sample["image"], **{"simu": self.simu, "pedestals": self.pedestals}
                )
            else:
                sample["image"] = self.transform(sample["image"])

        labels = {}
        if self.simu:
            dl1_parameters = {
                n: p for n, p in zip(self.dl1_param_names, dl1_params) if n not in self.mc_only_dl1_parameters
            }
            for t in self.targets:
                if t == "energy":
                    labels[t] = np.array([dl1_params["log_mc_energy"]], dtype=np.float32)
                elif t == "impact":
                    if self.group_by == "image":
                        labels[t] = np.array(
                            [
                                dl1_params["mc_core_x"] - dl1_params["tel_pos_x"],
                                dl1_params["mc_core_y"] - dl1_params["tel_pos_y"],
                            ],
                            dtype=np.float32,
                        )
                    else:
                        labels[t] = np.array(
                            [dl1_params["mc_core_x"], dl1_params["mc_core_y"]],
                            dtype=np.float32,
                        )
                elif t == "direction":
                    if self.group_by == "image":
                        labels[t] = np.array(
                            [
                                dl1_params["mc_alt"] - dl1_params["mc_alt_tel"],
                                dl1_params["mc_az"] - dl1_params["mc_az_tel"],
                            ],
                            dtype=np.float32,
                        )
                    else:
                        labels[t] = np.array(
                            [dl1_params["mc_alt"], dl1_params["mc_az"]],
                            dtype=np.float32,
                        )
                elif t == "xmax":
                    labels[t] = np.array([dl1_params["mc_x_max"]])
                elif t == "class":  # TODO replace by try except
                    labels[t] = self.particle_dict.get(dl1_params["mc_type"], -1)
                    if labels[t] == -1:
                        print(dl1_params["mc_type"])
                        print(self.hdf5_file_path)
                elif t == "domain_class":
                    labels[t] = self._get_domain_label()
                elif t == "autoencoder":
                    labels[t] = sample["image"]
        else:
            dl1_parameters = {
                n: p for n, p in zip(self.dl1_param_names, dl1_params) if n not in self.lst1_only_dl1_parameters
            }
            for t in self.targets:
                if t == "class":
                    labels[t] = REAL_DATA_ID
                elif t == "domain_class":
                    labels[t] = self._get_domain_label()
                elif t == "autoencoder":
                    labels[t] = sample["image"]

        if not self.train:
            dl1_parameters = {n: p for n, p in zip(self.dl1_param_names, dl1_params)}

        if labels:
            if self.target_transform:
                sample["label"] = {t: self.target_transform(label) for t, label in sample["label"].items()}
            else:
                sample["label"] = labels

        sample["dl1_params"] = dl1_parameters
        sample["transform_params"] = transform_params

        return sample

    def _get_domain_label(self):
        if self.domain == "source":
            return torch.tensor(self.domain_dict[SOURCE], dtype=torch.int64)
        elif self.domain == "target":
            return torch.tensor(self.domain_dict[TARGET], dtype=torch.int64)
        else:
            raise ValueError("Invalid domain. Must be 'source' or 'target'.")

    def _get_image_data(self, idx):
        raise NotImplementedError

    def filter_event(self, filter_dict):  # TODO: apply all filters at the same place (init of dataset)
        filter_mask = np.full(len(self.dl1_params), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # Apply filtering
        self._update_events(filter_mask)
        # update images
        self.update_images(filter_mask)

    def _update_events(self, filter_mask):
        self.dl1_params = self.dl1_params[filter_mask]
        self.unique_event_ids = np.unique(self.dl1_params[:]["event_id"])

    def _filter_image(self, filter_dict):
        filter_mask = np.full(len(self.images), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # Apply filtering
        self.update_images(filter_mask)
        self._update_events(filter_mask)

    def update_images(self, image_mask):
        """Abstract method implemented by Memory or File dataset to update their self.images member after
        some events are removed due to filters
        """
        raise NotImplementedError

    def filter_image(self, filter_dict):
        # TODO: why filter_image function and update_image as well ?
        raise NotImplementedError


class MemoryLSTDataset(BaseLSTDataset):
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
        mask_method=None,
        **kwargs,
    ):
        """Load all images and params in RAM as numpy array in initialization"""
        super(MemoryLSTDataset, self).__init__(
            hdf5_file_path,
            camera_type,
            group_by,
            targets,
            particle_dict,
            use_time,
            train,
            subarray,
            transform,
            target_transform,
            **kwargs,
        )

        self.mask_method = None
        self.images_masks = None

        # Check if "mask_method" belongs to the ginven names of cleaning techniques.
        if mask_method is not None:
            if mask_method in KNOWN_MASK_METHODS:
                self.mask_method = mask_method
            else:
                raise ValueError(f"Invalid mask method {mask_method}. Must be in {KNOWN_MASK_METHODS}")

        with tables.File(hdf5_file_path, "r") as hdf5_file:
            # Load images and peak times, apply cleaning masks to images
            self.images = hdf5_file.root[dl1_images_lstcam_key].col("image").astype(np.float32)[self.filtered_indices]
            self.images = np.nan_to_num(self.images)

            if self.use_time:
                self.times = (
                    hdf5_file.root[dl1_images_lstcam_key].col("peak_time").astype(np.float32)[self.filtered_indices]
                )
                self.times = np.nan_to_num(self.times, nan=NAN_TIME_VALUE)

            # Use precomputed image mask from lstchain
            if self.mask_method == "precomputed_lstchain":
                self.images_masks = hdf5_file.root[dl1_images_lstcam_key].col("image_mask")
                self.mask_channel(self.images_masks)

        # compute masks
        if self.mask_method == "tailcuts_standard_analysis":
            self.compute_tailcuts_standard_analysis(apply_mask=True)
        elif self.mask_method == "data_reduction_mask":
            self.compute_data_volume_reduction_masks(apply_mask=True)

        # remove empty images:
        non_empty_images_mask = self.find_non_empty_images_filter()
        self.update_images(non_empty_images_mask)
        self._update_events(non_empty_images_mask)

    def __getitem__(self, idx):
        return self._get_sample(idx)

    def compute_tailcuts_standard_analysis(self, apply_mask) -> None:
        """
        Compute masks for all images using tailcuts_clean method from ctapipe.
        Store the masks in the dataset (in self.clean_masks) and apply them to the images if apply_mask is True.
        It simulates the cleaning method used in the lstchain standard analysis, sometimes called tailcts 8,4.
        Check lstchain standard config
        `here <https://github.com/cta-observatory/cta-lstchain/blob/main/lstchain/data/lstchain_standard_config.json>`_

        Parameters
        ----------
        apply_mask : bool
            If True, apply the cleaning mask to all images in the dataset.
        """
        PICTURE_THRESH = 8
        BOUNDARY_THRESH = 4
        KEEP_ISOLATED_PIXELS = False
        MIN_NUMBER_PICTURE_NEIGHBORS = 2
        geometry = self.original_geometry
        masks = []
        for image in self.images:
            clean_mask = tailcuts_clean(
                geometry,
                image,
                PICTURE_THRESH,
                BOUNDARY_THRESH,
                KEEP_ISOLATED_PIXELS,
                MIN_NUMBER_PICTURE_NEIGHBORS,
            )
            masks.append(clean_mask)
        self.images_masks = np.stack(masks)
        if apply_mask:
            self.mask_channel(self.images_masks)

    def compute_data_volume_reduction_masks(self, apply_mask) -> None:
        """
        Compute masks for all images using data volume reduction method (lstchain).
        Store the masks in the dataset (in self.clean_masks) and apply them to the images if apply_mask is True.
        Data reduction method combines a threshold and a morphological dilation.
        Check https://github.com/cta-observatory/cta-lstchain/blob/main/lstchain/reco/volume_reducer.py
        Parameters:
        ----------
        apply_mask: (bool) If True, apply the cleaning mask to all images in the dataset.
        """
        masks = []
        geometry = self.original_geometry
        for image in self.images:
            mask = dvr.get_selected_pixels(
                image, dvr.CHARGE_THRESHOLD, dvr.NUMBER_DILATIONS, geometry, dvr.MIN_NUMBER_PIXELS
            )
            masks.append(mask)
        self.images_masks = np.stack(masks)
        if apply_mask:
            self.mask_channel(self.images_masks)

    def find_non_empty_images_filter(self):
        """
        Filter images that are empty (i.e. all pixels are 0)
        Parameters
        ----------
        dataset (Dataset): the dataset to filter

        Returns
        -------
        (list of bool): the mask to filter the data
        """
        return np.any(self.images, axis=(1))

    def _get_image_data(self, idx):
        """Return image + peak_times `idx` from the loaded images."""
        # TODO: since the images and params are loaded as numpy arrays, we should be able to just index the array with `idx`.
        if isinstance(idx, np.ndarray):
            data = np.zeros((len(idx), self.images.shape[1]))
            time = None
            if self.use_time:
                time = np.zeros((len(idx), self.times.shape[1]))
            for i, ind in enumerate(idx):
                if ind > -1:
                    indice = np.argwhere(self.filtered_indices == ind).item()
                    data[i] = self.images[indice]
                    if self.use_time:
                        time[i] = self.times[indice]
            data = (data,)
            if self.use_time:
                data += (time,)
        else:
            data = (self.images[idx],)
            if self.use_time:
                data += (self.times[idx],)
        return data

    def filter_image(self, filter_dict):
        self._filter_image(filter_dict)

    def update_images(self, image_mask):
        self.images = self.images[image_mask]
        if self.times is not None:
            self.times = self.times[image_mask]
        if self.images_masks is not None:
            self.images_masks = self.images_masks[image_mask]
        self.filtered_indices = np.arange(len(self.images))

    def mask_channel(self, images_masks):
        """
        Apply cleaning masks from DL1 file to all images and times (if times provided) in the dataset.

        Parameters
        ----------
            images_masks: (list) a list of booleans with `False` when no remarkable event on pixel and `True`
            when an event passes the cleaning operation. Cleaning masks are provided in the
            DL1 file as a column named `image_mask` of the `astropy.table.table.Table`.

        Returns
        -------
            Cleaned images and times channels with the same pixel size as the original images. Pixels with no signal are set to 0
            and pixels with signal are kept unchanged.

            If times are provided, the cleaned times are returned as well.
            Contrary to images, times pixels are set -1 when no signal is detected.
        """
        self.images = self.images * images_masks
        if self.times is not None:
            self.times[images_masks == 0] = NAN_TIME_VALUE


class FileLSTDataset(BaseLSTDataset):
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
        """Loads the images, times and parameters in the __getitem__ method"""
        super(FileLSTDataset, self).__init__(
            hdf5_file_path,
            camera_type,
            group_by,
            targets,
            particle_dict,
            use_time,
            train,
            subarray,
            transform,
            target_transform,
            **kwargs,
        )

    def __getitem__(self, idx):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, "r")
        return self._get_sample(idx)

    def _get_image_data(self, idx):
        """Load the images and params at index `idx`  from disk"""
        image_id = self.filtered_indices[idx]
        if isinstance(image_id, np.ndarray):
            image_size = self.hdf5_file.root[dl1_images_lstcam_key].col("image").shape[1]
            data = np.zeros((len(image_id), image_size))
            time = None
            if self.use_time:
                time = np.zeros((len(image_id), image_size))
            for i, ind in enumerate(image_id):
                if ind > -1:
                    data[i] = np.nan_to_num(
                        self.hdf5_file.root[dl1_images_lstcam_key].col("image")[ind].astype(np.float32)
                    )
                    if self.use_time:
                        time[i] = np.nan_to_num(
                            self.hdf5_file.root[dl1_images_lstcam_key].col("peak_time")[ind].astype(np.float32),
                            nan=NAN_TIME_VALUE,
                        )
            data = (data,)
            if self.use_time:
                data += time
        else:
            data = (
                np.nan_to_num(self.hdf5_file.root[dl1_images_lstcam_key].col("image")[image_id].astype(np.float32)),
            )
            if self.use_time:
                time = np.nan_to_num(
                    self.hdf5_file.root[dl1_images_lstcam_key].col("peak_time")[image_id].astype(np.float32),
                    nan=NAN_TIME_VALUE,
                )
                data += (time,)
        return data

    def filter_image(self, filter_dict):
        """Load all images of the file from disk, and apply filers so that only valid images are kept when
        iterating on the dataset afterwards.
        """
        self._open_file()
        self._filter_image(filter_dict)
        self._close_file()

    def update_images(self, image_mask):
        self.filtered_indices = self.filtered_indices[image_mask]

    def _open_file(self):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, "r")
            self.images = np.nan_to_num(self.hdf5_file.root[dl1_images_lstcam_key].col("image")[self.filtered_indices])
            self.times = np.nan_to_num(
                self.hdf5_file.root[dl1_images_lstcam_key].col("peak_time")[self.filtered_indices],
                nan=NAN_TIME_VALUE,
            )

    def _close_file(self):
        if self.hdf5_file is not None:
            self.hdf5_file.close()
            self.hdf5_file = None
            self.images = None
            self.times = None
