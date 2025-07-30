import multiprocessing as mp
import os
import random
from itertools import islice

import torch
import tqdm
from PIL import Image
from torch.utils.data import Dataset
from typing_extensions import deprecated

from gammalearn.configuration.constants import SOURCE, TARGET
from gammalearn.data.transforms import GLearnCompose


@deprecated("Digit's Datasets and DataModules are deprecated and will be removed in a future release!")
class DigitMixDataset(Dataset):
    """
    Dataset class to load images from several classic image digits dataset : mnist, mnistm, usps, svhn

    Parameters
    ----------
        paths: (list) Paths to the datasets. TODO: It can only be used if the list has a single element
        dataset_parameters: (dict) The corresponding parameters to the datasets. These parameters will be applied to all
        datasets.
        transform: The transforms applied to the images.
        target_transform: The transforms applied to the targets.
        train: (bool) If train is 'True', returns the train datasets, otherwise returns the test datasets.
        domain: (str) In the domain adaptation context, gives an extra domain label 'source' or 'target'. Otherwise, set
        to 'None' (default).
        max_files: (int) The number of images to load in each dataset. If set to '-1' (default), all images and targets
        will be loaded.
    """

    def __init__(
        self,
        paths,
        dataset_parameters,
        transform=None,
        target_transform=None,
        train=True,
        domain=None,
        max_files=-1,
        num_workers=10,
    ):
        self.paths = paths
        self.dataset_parameters = dataset_parameters
        self.camera_geometry = None  # Mandatory
        self.targets = list(dataset_parameters["targets"])
        self.train = train
        self.domain = "source" if domain is None else domain
        self.num_workers = num_workers if num_workers > 0 else 1
        self.max_files = -1 if max_files is None else max_files

        self.dataset = []
        for path in self.paths:  # TODO: Currently working only for paths[0], cf multiprocessing data loading
            self.dataset += self.load_dataset(path)

        self.transform = transform
        self.target_transform = target_transform

    def _get_domain_label(self):
        if self.domain == "source":
            return torch.tensor(self.dataset_parameters["domain_dict"][SOURCE], dtype=torch.int64)
        elif self.domain == "target":
            return torch.tensor(self.dataset_parameters["domain_dict"][TARGET], dtype=torch.int64)
        else:
            raise ValueError("Invalid domain. Must be 'source' or 'target'.")

    def load_dataset(self, path):
        """Load the images in the dataset located at `path`.

        .. code-block:: text

            Example: /uds_data/.../mnist
            Inside the data set folder, must be "train" and "test" subfolders
                /uds_data/.../mnist
                                   /train
                                        /image_list.txt -> contains the relative path towards the images files (*.png) and their label
                                        images/*.png
                                   /test
                                        same structure than in train
            (This format was made to have a similar structure for all possible datasets)

        Returns
        -------
        list[np.ndarray]
            The loaded dataset
        """
        split = "train" if self.train else "test"
        with open(os.path.join(path, split, "image_list.txt")) as f:
            lines = f.readlines()
            # Truncate the list if 'max_files' is defined
            if self.max_files > 0:
                random.shuffle(lines)
                lines = lines[: self.max_files]

            # Split the main list into 'num_workers' sublists
            a = len(lines) // self.num_workers
            b = len(lines) % self.num_workers
            length_to_split = self.num_workers * [a]
            length_to_split[-1] += b
            lines_iter = iter(lines)
            lines_list = [list(islice(lines_iter, elem)) for elem in length_to_split]

            # Multiprocessing
            ctx = mp.get_context("spawn")
            pool = ctx.Pool(processes=self.num_workers)

            dataset_list = list(pool.imap(self.load_subset, lines_list))
            dataset = sum(dataset_list, [])
            # dataset = self.load_subset(os.path.join(path, split), lines)

        return dataset

    def load_subset(self, lines, path=None):
        subset = []

        # TODO: makes it more generic: include multiple paths (partial func ?)
        split = "train" if self.train else "test"
        path = os.path.join(self.paths[0], split)

        for i in tqdm.tqdm(range(len(lines))):
            img_path = lines[i].split(" ")[0]
            label = int(lines[i].split(" ")[1])
            img_pil = Image.open(os.path.join(path, img_path))
            data = (img_pil.copy(), label)
            subset.append(data)
            img_pil.close()

        return subset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        data = self.dataset[item]
        image, label_class = data[0], data[1]

        if self.transform:
            if isinstance(self.transform, GLearnCompose):
                image, transform_params = self.transform(image)
            else:
                image = self.transform(image)
                transform_params = {}

        labels = {}
        for t in self.targets:
            if t == "class":
                labels["class"] = torch.tensor(label_class)
            elif t == "domain_class":
                labels["domain_class"] = self._get_domain_label()
            elif t == "autoencoder":
                labels["autoencoder"] = image.clone()

        if self.target_transform:
            pass  # TODO: TO BE IMPLEMENTED

        return {"image": image, "label": labels, "transform_params": transform_params}
