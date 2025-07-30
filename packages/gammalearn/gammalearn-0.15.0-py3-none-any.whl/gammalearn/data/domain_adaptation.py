from torch.utils.data import Dataset

from gammalearn.data.telescope_geometry import fetch_dataset_geometry


class DomainAdaptationDataset(Dataset):
    """
    Inputs two datasets and output a sample in the form of a tuple. Elements part of the smallest dataset are looped.
    """

    def __init__(self, source_dataset, target_dataset):
        super().__init__()
        # assert len(source_dataset) == len(target_dataset)
        self.source_dataset = source_dataset
        self.target_dataset = target_dataset
        self.camera_geometry = None

    def __len__(self):
        # If __len__ returns len(self.source_dataset) + len(self.target_dataset), the idx will range from 0 to
        # len(self.source_dataset) + len(self.target_dataset) - 1, which is not compatible with the currently
        # implemented __getitem__ function
        return max(len(self.source_dataset), len(self.target_dataset))

    def __getitem__(self, idx):
        idx_source = idx % len(self.source_dataset)
        idx_target = idx % len(self.target_dataset)
        sample_source = {k + "_source": v for k, v in self.source_dataset[idx_source].items()}
        sample_target = {k + "_target": v for k, v in self.target_dataset[idx_target].items()}
        sample = {**sample_source, **sample_target}

        return sample


class GlearnDomainAdaptationDataset(DomainAdaptationDataset):
    """
    Equivalent to the vision domain adaptation dataset but contains a cmaera geometry attribute related to the LST images.
    """

    def __init__(self, source_dataset, target_dataset):
        super(GlearnDomainAdaptationDataset, self).__init__(source_dataset, target_dataset)
        camera_geometry_source = fetch_dataset_geometry(source_dataset)
        camera_geometry_target = fetch_dataset_geometry(target_dataset)
        assert camera_geometry_source == camera_geometry_target, "Source and target camera geometry must be the same."
        self.camera_geometry = camera_geometry_source
