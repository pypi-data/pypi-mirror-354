from __future__ import annotations
from torch.utils.data import Dataset, DataLoader
from typing import Union, Tuple, List, Dict, Callable, Sequence, Literal
from pathlib import Path
from deepvisiontools.data.data_reader.readers import (
    BaseReader,
    CocoReader,
    ANNOTATION_TYPE_DICT,
    SemanticReader,
)
from deepvisiontools.preprocessing.preprocessing import build_preprocessing
from deepvisiontools.preprocessing.image import (
    load_image,
    save_image,
    save_mask,
    load_mask,
)
from deepvisiontools import Configuration
from deepvisiontools.formats import (
    BaseFormat,
    BatchedFormat,
    SemanticMaskFormat,
    SemanticMaskData,
)
from deepvisiontools.utils import visualization
from torch import Tensor
from torchvision.transforms.v2 import Transform
from deepvisiontools.data.augmentation_class import Augmentation
import torchvision.transforms.v2 as T
import torch
import copy
from random import shuffle
import deepvisiontools.data.errors as er
from tqdm import tqdm
import json


class DeepVisionDataset(Dataset):
    """Detection dataset class for deepvisiontools : load and return image, annotation, image name.

    Args:
        dataset_path (Union[str, Path]): path to dataset folder.
        reader (BaseReader, optional): Class to read data from dataset folder. Defaults to CocoReader.
        preprocessing (Callable, optional): Preprocessing images (normalization). Defaults to build_preprocessing().
        augmentation (List[Transform], optional): Augmentation to apply to images / annotations. Must be from torchvision.transforms.v2.Transform Defaults to None.
        label_converter (Dict[int, int], optional): Convert labels to another value. For e.g : {0: 2, 1: 5} etc. Defaults to None.

    Example:
    ----------

    .. highlight:: python
    .. code-block:: python

        >>> from deepvisiontools import DeepVisionDataset
        >>> data_path = \"path/to/data\"
        >>> dataset = DeepVisionDataset(data_path)
        >>> image, target, image_name = dataset[1]
        >>> print(type(image), type(target), type(image_name))
        <class 'torch.Tensor' >, <class 'BboxFormat' >, <class 'str'>
        >>> print(image.shape, target.size, image_name)
        torch.Size([3,512,512]), 5, 'img_01.png'


    Attributes
    ----------

    Attributes:
        - dataset_path (``Path``): path to dataset folder.
        - reader (``BaseReader``): Class to read data from dataset folder. Defaults to CocoReader.
        - preprocessing (``Callable``): Preprocessing images (normalization). Defaults to build_preprocessing().
        - augmentation (``List[Transform]``): Augmentation to apply to images / annotations. Must be from torchvision.transforms.v2.Transform Defaults to None.
        - category_ids (``Dict[int, str]``): Dict that associate a name to a category label index. Defaults is equal to self.reader.category_ids
        - label_converter (``Dict[int, int]``): Convert labels to another value. For e.g : {0: 2, 1: 5} etc. Defaults to None.


    **Methods**:
    """

    def __init__(
        self,
        dataset_path: Union[str, Path],
        reader: Union[BaseReader, None] = None,
        preprocessing: Callable = build_preprocessing(),
        augmentation: List[Transform] = None,
        label_converter: Dict[int, int] = None,
        category_ids: Union[Dict[int, str], None] = None,
    ):

        self.dataset_path = (
            dataset_path if isinstance(dataset_path, Path) else Path(dataset_path)
        )
        assert (
            self.dataset_path.exists()
        ), f"{self.dataset_path} is not a valid dataset folder. Please check that folder exists."
        # Choose default reader between CocoReader and SemanticReader if None is provided for reader
        if reader != None:
            self.reader: BaseReader = reader(dataset_path)
        elif Configuration().data_type == "semantic_mask":
            self.reader = SemanticReader(dataset_path)
        else:
            self.reader = CocoReader(dataset_path)
        self.preprocessing = preprocessing
        self.augmentation = augmentation
        self._category_ids = category_ids if category_ids else self.reader.category_ids
        self.label_converter = label_converter
        self._img_dir = self.dataset_path / "images"
        self._device = Configuration().device
        # The following is to handle splitting
        self._indexes = list(range(len(self.reader)))

    @property
    def category_ids(self):
        return self._category_ids

    @category_ids.setter
    def category_ids(self, val):
        self.reader.category_ids = val
        self._category_ids = val

    def __getitem__(self, idx: int):
        elem = self.reader[self._indexes[idx]]
        img_name: str = elem[0]
        target: BaseFormat = elem[1]
        # Rename / regroup categories if wanted
        if self.label_converter != None:
            if isinstance(target, SemanticMaskFormat):
                # change mask labels as per convert dict
                new_data = copy.deepcopy(target.data.value)
                for k, v in self.label_converter:
                    new_data[target.data.value == k] = v
                target = SemanticMaskData(new_data)
                target = SemanticMaskFormat(target)
            else:
                new_labels = [self.label_converter[l] for l in target.labels]
                target = type(target)(target.data, new_labels)

        image = load_image(self._img_dir / img_name)
        image = image.to(self._device)
        target.device = self._device

        if self.augmentation != None:
            augment = Augmentation(self.augmentation)
            image, target = augment(image, target)

        if self.preprocessing != None:
            image = self.preprocessing(image)

        target, _ = target.sanitize()
        return image, target, img_name

    def __len__(self) -> int:
        return len(self._indexes)

    def __iter__(self):
        for x in range(len(self)):
            yield self[x]

    def split(
        self, sequence: Sequence[float, float, float]
    ) -> Tuple[DeepVisionDataset, DeepVisionDataset, DeepVisionDataset]:
        """split dataset in 3 new datasets according to proportions

        Args:
            sequence (Sequence[float, float, float]): proportions to split the dataset into. Sum must be 1.

        Example:
        ----------
        .. highlight:: python
        .. code-block:: python

            >>> dataset = DeepVisionDataset("path/to/dataset")
            >>> train_dataset, valid_dataset, test_dataset = dataset.split((0.6, 0.2, 0.2))
        """
        seq_sum = sum(sequence)
        assert round(seq_sum, 3) == 1, "sequence sum is not equal to 1."
        idx = copy.copy(self._indexes)
        shuffle(idx)
        stop1 = int(sequence[0] * len(idx))
        stop2 = int(sum(sequence[0:2]) * len(idx))
        # stop3 = int(seq_sum * len(idx))
        if stop2 > len(idx):
            stop2 -= len(idx) - stop2
        dataset1 = copy.deepcopy(self)
        dataset1._indexes = idx[0:stop1]
        dataset2 = copy.deepcopy(self)
        dataset2._indexes = idx[stop1:stop2]
        dataset3 = copy.deepcopy(self)
        if len(idx[stop2:]) == 0:
            dataset3 = None
        else:
            dataset3._indexes = idx[stop2:]
        return dataset1, dataset2, dataset3

    def keep_indexes(self, indexes: Union[list, slice, Tensor]) -> DeepVisionDataset:
        """Filter dataset by keeping only indices given in arg.

        Args:
            indexes (``Union[list, slice, Tensor]``): can be slice, Tensor or list. To use slice please use : slice(i, j) with i, j desired slice indexes in arg.
        """
        dataset = copy.deepcopy(self)
        if isinstance(indexes, Tensor):
            assert (
                indexes.dim() == 1
            ), f"Must use Tensor of dim 1 for indexes, got {indexes.shape}"
            indexes = indexes.tolist()
        indx = torch.tensor(dataset._indexes)[indexes].tolist()
        dataset._indexes = indx
        return dataset

    def export_dataset(
        self,
        destination_folder: Union[str, Path],
        number_visu: Union[Literal["all"], int] = "all",
        file_extension: str = "",
    ):
        """Export dataset accordingly to BaseReader class. For example CocoReader will export in following structure:
        Dataset Name -> Image_dir, coco_annotations.json

        Args:
            destination_folder (Union[str, Path]): Path to new dataset folder.
            number_visu (Union[Literal[&quot;all&quot;], int], optional): number of visualization to create. If "all" will derive all of them. Defaults to "all".
            file_extension (str, optional): if requires a specific file extension. If "" will use BaseReader's. Defaults to "".
        """
        if file_extension == "":
            file_extension = self.reader.annotation_file_type
        destination_folder = (
            destination_folder
            if isinstance(destination_folder, Path)
            else Path(destination_folder)
        )
        number_visu = len(self) if number_visu == "all" else number_visu
        img_folder = destination_folder / "images"
        annot_folder = destination_folder / "annotations"
        visu_folder = destination_folder / "visualizations"
        if number_visu > 0:
            visu_folder.mkdir(parents=True, exist_ok=True)
        img_folder.mkdir(parents=True, exist_ok=True)
        annot_folder.mkdir(parents=True, exist_ok=True)
        for img, target, img_name in tqdm(
            self, total=len(self), desc="Exporting dataset : "
        ):
            visu_saved = 0
            if visu_saved < number_visu:
                visu_path = visu_folder / f"visu__{img_name}"
                visualization(img, target, self.category_ids, save_path=visu_path)
            save_image(img, img_folder / img_name)
            _, export_target = self.reader.export_annotation(
                img_name, img, target, self.category_ids
            )
            annot_file_path = annot_folder / f"{Path(img_name).stem}.{file_extension}"
            if ANNOTATION_TYPE_DICT[file_extension] == "file":
                with open(annot_file_path, "w") as f:
                    if isinstance(export_target, dict):
                        json.dump(export_target, f)
                    else:
                        f.write(export_target)
            elif ANNOTATION_TYPE_DICT[file_extension] == "mask":
                save_mask(export_target, annot_file_path)
        self.reader.group_export(
            annot_folder,
            destination_folder,
        )


# TODO : add collate augmentations functions : mosaic


class DeepVisionLoader(DataLoader):
    """Child class of ``DataLoader`` that batchify images and BaseFormats. DetectionLoader support any features from torch Dataloaders (Sampler, etc..).

    Args:
        *args
        *kwargs

    Example:
    ----------
    .. highlight:: python
    .. code-block:: python

        >>> from deepvisiontools import DeepVisionLoader
        >>> loader = DeepVisionLoader(dataset, batch_size=2)
        >>> for batch in loader:
        >>>     img, target, img_name = batch


    **Methods**:
    """

    def __init__(self, *args, **kwargs):
        self.batch_augmenter = kwargs.pop("batch_augmenter", None)
        super().__init__(collate_fn=self.collate_fn, *args, **kwargs)

    def collate_fn(
        self, batch: List[Tuple[str, Tensor, BaseFormat]]
    ) -> Tuple[Tensor, BaseFormat]:
        """
        Args:
            batch (``List[Tuple[Tensor, BaseFormat]]``): List of pairs image/target.

        Returns:
            ``Tuple[Tensor, BatchedFormats]``:
                - Batch images (N, 3, H, W).
                - BaseFormats wrapped into BatchedFormats class.
        """
        images = [triplet[0] for triplet in batch]
        targets = [triplet[1] for triplet in batch]
        names = {i: triplet[2] for i, triplet in enumerate(batch)}
        images, targets = self.pad_to_larger(images, targets)
        er.check_images_targets_size(images, targets)
        batch_images = torch.stack(images).to(Configuration().device)
        batch_targets = BatchedFormat(targets)

        # apply batch_augmenter if not None
        if self.batch_augmenter != None:
            batch_images, batch_targets = self.batch_augmenter.get_new_batch(
                batch_images, batch_targets
            )

        return batch_images, batch_targets, names

    def pad_to_larger(
        self, images: List[Tensor], targets: List[BaseFormat]
    ) -> Tuple[List[Tensor], List[BaseFormat]]:
        """Pad images and targets to larger image size.

        Args:
            images (``List[Tensor]``): Images.
            targets (``List[BaseFormat]``): Targets.
        """
        # get max borders sizes
        larger_width = max([image.shape[-1] for image in images])
        larger_height = max([image.shape[-2] for image in images])
        padded_images, padded_targets = [], []

        # for each image pad image & target
        for i, image in enumerate(images):
            t = int((larger_height - image.shape[-2]) / 2)
            l = int((larger_width - image.shape[-1]) / 2)
            r = int((larger_width - image.shape[-1]) - l)
            b = int((larger_height - image.shape[-2]) - t)
            # Order of t, l, b, r changes again in torchvision
            padder = T.Pad((l, t, r, b))
            padded_images.append(padder(image))
            padded_targets.append(targets[i].pad_to((larger_height, larger_width))[0])

        return padded_images, padded_targets

    def visualize(self, dir_path: Union[str, Path]):
        """Generate visualization through DeepVisionLoader. Can be useful to test batch_augmenter effect."""
        dir_path = dir_path if isinstance(dir_path, Path) else Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
        for i, item in tqdm(enumerate(self), total=len(self)):
            imgs, targs, _ = item
            for j in range(imgs.shape[0]):
                visualization(
                    imgs[j].to(torch.uint8),
                    targs.formats[j],
                    save_path=dir_path / f"Batch_{i}__img_{j}.png",
                )
