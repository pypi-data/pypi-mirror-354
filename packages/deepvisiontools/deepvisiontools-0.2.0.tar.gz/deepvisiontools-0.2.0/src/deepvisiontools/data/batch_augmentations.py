from deepvisiontools.formats import BaseFormat, BatchedFormat, SemanticMaskFormat
import torch
from torch import Tensor
from abc import ABC, abstractmethod
from typing import Tuple, Union, Literal, List
from random import shuffle, uniform
from deepvisiontools import Configuration
import itertools
from torchvision.transforms.v2 import Resize
import copy


class AbstractBatchAugmenter(ABC):
    """Abstract class for augmentation within DataLoader (combine elements of batch together such as mosaic type augmentation)
    Note : these augmentations always come after normal augmentations that are implemented in Dataset instead of dataloader for this one.
    """

    @abstractmethod
    def get_new_batch(
        self, images_batch: Tensor, targets_batch: BatchedFormat
    ) -> Tuple[Tensor, BatchedFormat]:
        pass


MOSAIC_CONVERTER = {
    1: (1, 1),
    2: (1, 2),
    4: (2, 2),
    6: (2, 3),
    8: (2, 4),
    9: (3, 3),
    12: (3, 4),
}


class MosaicBatchAugmenter(AbstractBatchAugmenter):
    """This Batch augmentation generate a mosaic containing n images from a batch (mix some patch of images / targets into one image).
    If the number of image is larger than batch size shift to smaller possibility (for e.g. n = 4 batch_size=3 -> n becomes 2).
    if number of image to be mixed is smaller than batch_size, create new mosaics if possible : for e.g batchsize = 5, n=2 -> generate 2 mosaics from the first 2 images, then an additional 2 images with remaining, and finally the remaining is 1.
    The remaining images are left untouched

        Args:
            mixed_img_numb (``Literal[1, 2, 4, 6, 8, 9, 12]``, **optional**): Number of img per mosaic. Defaults to 2.
            probability (``float``, **optional**): _description_. Defaults to 0.5.
    """

    def __init__(
        self,
        mixed_img_numb: Literal[1, 2, 4, 6, 8, 9, 12] = 2,
        probability: float = 0.5,
    ):

        assert mixed_img_numb in list(
            MOSAIC_CONVERTER.keys()
        ), f"Wrong argument in MosaicBatchAugmenter, mixed_img_num must be one of [1, 2, 4, 6, 8, 9, 12], got {mixed_img_numb}"
        self.mixed_img_number = mixed_img_numb
        self._used_mixed_img_nb = mixed_img_numb
        self.probability = probability
        self._device = Configuration().device
        self._imgs_shape = None
        self._mosaic_shape = None
        self._resizer = None

    def _adapt_to_batch(self, images_batch: Tensor):
        assert (
            images_batch.dim() == 4
        ), f"To use MosaicBatchAugmenter, batches of images must have dim=4 (N, 3, H, W), got {images_batch.shape}"
        num_img = images_batch.shape[0]
        h, w = images_batch.shape[-2:]
        option_list = [1, 2, 4, 6, 8, 9, 12]
        # adapt batch size to option of nb of mixed img
        while self._used_mixed_img_nb > num_img:
            self._used_mixed_img_nb = option_list[
                option_list.index(self._used_mixed_img_nb) - 1
            ]
        self._imgs_shape = images_batch.shape[-2:]
        # adapt mosaic shape to largest between h and w of images
        m_shape = MOSAIC_CONVERTER[self._used_mixed_img_nb]
        if h > w:
            m_shape = (max(m_shape), min(m_shape))
        self._mosaic_shape = m_shape
        self._resizer = Resize((h, w))

    def _reset(self):
        self._used_mixed_img_nb = self.mixed_img_number
        self._mosaic_shape = None
        self._resizer = None

    def _get_mixing_index(self, images_batch: Tensor) -> Tuple[Tensor, Tensor]:
        num_imgs = images_batch.shape[0]
        index = list(range(num_imgs))
        shuffle(index)
        kept_index = index
        mixing_index = []
        while len(kept_index) >= self._used_mixed_img_nb:
            mixing_index.append(kept_index[: self._used_mixed_img_nb])
            kept_index = kept_index[self._used_mixed_img_nb :]
        return mixing_index, kept_index

    def _generate_batchs_lists(
        self, images_batch: Tensor, targets_batch: BatchedFormat
    ) -> Tuple[List[Tensor], List[BatchedFormat], Tensor, BatchedFormat]:
        mixing_index, kept_indexes = self._get_mixing_index(images_batch)
        # split batch into the ones that are kept and the ones to be mixed.
        if kept_indexes != []:
            images2keep: Tensor = images_batch[kept_indexes]
            targets2keep: BatchedFormat = targets_batch[kept_indexes]
        else:
            images2keep = torch.empty([0])
            targets2keep = BatchedFormat([])

        images_batches_to_mix: list = [
            images_batch[mix_batch] for mix_batch in mixing_index
        ]  # list of Tensor of shape [n_mix, h, w]
        targets_batches_to_mix: list = [
            targets_batch[mix_batch] for mix_batch in mixing_index
        ]  # list of corresponding BatchedFormats
        return images_batches_to_mix, targets_batches_to_mix, images2keep, targets2keep

    def _get_crop_coords_lists(self):
        h, w = self._imgs_shape
        h_divider, w_divider = self._mosaic_shape
        crop_coords_list = []
        h_step = float(h) / h_divider
        w_step = float(w) / w_divider
        for i, j in itertools.product(list(range(h_divider)), list(range(w_divider))):
            t_c, l_c, h_c, w_c = i * h_step, j * w_step, h_step, w_step
            crop_coords_list.append((round(t_c), round(l_c), round(h_c), round(w_c)))
        return crop_coords_list

    def _mix_batch(
        self,
        batch_img: Tensor,
        batch_targ: BatchedFormat,
        crops_coords: List[Tuple[int, int, int, int]],
    ):
        num_imgs = batch_img.shape[0]
        cycle = list(range(num_imgs))  # use this for all imgs/targs permutations
        cycles = []
        for i in range(len(cycle)):
            first_elem = cycle.pop(0)
            cycle.append(first_elem)
            cycles.append(copy.deepcopy(cycle))

        new_batch_img = []
        new_batch_targs = []
        for cy in cycles:
            new_img, new_tar = self._get_img_targ_from_cycle_of_crops(
                batch_img, batch_targ, cy, crops_coords
            )
            new_batch_img.append(copy.deepcopy(new_img))
            new_batch_targs.append(copy.deepcopy(new_tar))
        return torch.stack(new_batch_img), BatchedFormat(new_batch_targs)

    def _get_img_targ_from_cycle_of_crops(
        self,
        batch_img: Tensor,
        batch_targ: BatchedFormat,
        cycle: list,
        crops_coords: list,
    ):
        list_imgs = [batch_img[i] for i in cycle]
        list_targs = BatchedFormat([batch_targ.formats[i] for i in cycle])
        new_img = torch.zeros((3, *self._imgs_shape))
        new_targ: BaseFormat = type(list_targs.formats[0]).empty(
            canvas_size=list_targs.formats[0].canvas_size
        )
        ori_h, ori_w = new_targ.canvas_size
        if isinstance(new_targ, SemanticMaskFormat):
            new_targ = new_targ.generate_scores_from_mask()
        for im, tar, crop_coord in zip(list_imgs, list_targs, crops_coords):
            t, l, h, w = crop_coord
            new_img[:, t : t + h, l : l + w] = im[:, t : t + h, l : l + w]
            crop_targ = tar.crop(t, l, h, w)[0]
            t_pad, l_pad, r_pad, b_pad = t, l, ori_w - l - w, ori_h - t - h
            crop_targ = crop_targ.pad(t_pad, l_pad, r_pad, b_pad)[0]
            if isinstance(crop_targ, SemanticMaskFormat):
                crop_targ = crop_targ.generate_scores_from_mask()
            new_targ += crop_targ
        return new_img, new_targ

    def get_new_batch(self, images_batch: Tensor, targets_batch: BatchedFormat):
        # ======= Prepare
        self._adapt_to_batch(images_batch)
        # if proba fails or if image nb to mix is 1, don't do mixing
        if uniform(0, 1) > self.probability or self._used_mixed_img_nb == 1:
            return images_batch, targets_batch
        # get to be mixed imgs and targs as well as to be kept images and targs
        images_batches_to_mix, targets_batches_to_mix, images2keep, targets2keep = (
            self._generate_batchs_lists(images_batch, targets_batch)
        )
        # ======= Handle mixing
        crops_coords = self._get_crop_coords_lists()
        final_batchs_img_mixed = []
        final_batchs_tars_mixed = []
        for batch_img, batch_targ in zip(images_batches_to_mix, targets_batches_to_mix):
            new_img, new_targ = self._mix_batch(batch_img, batch_targ, crops_coords)
            final_batchs_img_mixed.append(new_img)
            final_batchs_tars_mixed.append(new_targ)
        final_imgs_mixed = torch.cat(final_batchs_img_mixed).to(Configuration().device)
        final_targs_mixed = BatchedFormat.cat(final_batchs_tars_mixed)
        # aggragate untouched and mixed
        if targets2keep.formats != []:
            new_img_fullbatch = torch.cat([final_imgs_mixed, images2keep])
            new_tar_fullbatch = BatchedFormat.cat([final_targs_mixed, targets2keep])
        else:
            new_img_fullbatch = final_imgs_mixed
            new_tar_fullbatch = final_targs_mixed
        # ======= reset for futu uses
        self._reset()
        return new_img_fullbatch, new_tar_fullbatch
