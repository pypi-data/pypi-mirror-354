import torch
import torchvision.transforms.v2 as T
from torchvision.transforms.v2 import Transform
from typing import Sequence, Union, Tuple
import random as rd
from pathlib import Path
from deepvisiontools.preprocessing.image import load_image
from torchvision.tv_tensors import BoundingBoxes, Mask
from torch import Tensor
import copy


class RandomCropAndResize(Transform):
    """
    With a given probability, apply RandomCrop and Resize from torchvision.transforms.v2.
    NB : here we resize only and systematically if cropped.

    Args:
        crop (``Union[int, Sequence[int]]``): Size to crop
        resize (``Union[int, Sequence[int]]``): Size to resize
        p (``float``, **optional**): probability. Defaults to 0.5.


    **Methods**:
    """

    def __init__(
        self,
        crop: Union[int, Sequence[int]],
        resize: Union[int, Sequence[int]],
        p=0.5,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.p = p
        self.crop = T.RandomCrop(crop)
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            pass
        else:
            inputs = self.crop.forward(inputs)
            inputs = self.resize.forward(inputs)
        return inputs


class RandomCenterCropAndResize(Transform):
    """
    With a given probability, apply CenterCrop and Resize from torchvision.transforms.v2.
    NB : here we resize only and systematically if cropped.

        Args:
            crop (``Union[int, Sequence[int]]``): Size to crop
            resize (``Union[int, Sequence[int]]``): Size to resize
            p (``float``, **optional**): probability. Defaults to 0.5.
    """

    def __init__(self, crop: Sequence[int], resize: Sequence[int], p=0.5, **kwargs):
        super().__init__(**kwargs)
        self.p = p
        self.crop = T.CenterCrop(crop)
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            pass
        else:
            inputs = self.crop.forward(inputs)
            inputs = self.resize.forward(inputs)
        return inputs


class RandomPadAndResize(Transform):
    """
    With a given probability, apply Pad and Resize from torchvision.transforms.v2. This looks like a zoom out effect by decreasing spatial resolution.
    NB : here we resize only and systematically if Padded.

        Args:
            MaxPad (``Union[int, Sequence[int]]``): maximum padding bounds can be int for common padding bound for all borders or sequence of 4 ints for (t, l, b, r)
            resize (``Tuple[int, int]``): Size to resize
            p (``float``, **optional**): probability to apply transformation. Defaults to 0.5.
    """

    def __init__(
        self,
        maxpad: Sequence[int],
        resize: Tuple[int, int],
        p=0.5,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.p = p
        self.max_pad = (maxpad,) * 4 if isinstance(maxpad, int) else maxpad
        self.resize = T.Resize(resize)

    def forward(self, *inputs):
        if torch.rand(1) >= self.p:
            return inputs
        else:
            t = rd.randrange(0, self.max_pad[0])
            l = rd.randrange(0, self.max_pad[1])
            r = rd.randrange(0, self.max_pad[2])
            b = rd.randrange(0, self.max_pad[3])
            padder = T.Pad([t, l, b, r])
            inputs = padder(inputs)
            inputs = self.resize(inputs)
        return inputs


class RandomChangeBackground(Transform):
    """With a given probability p, swap image background. New background is taken from an image folder for which path is provided.
    Note 1 : it is implemented only for instance_mask, semantic_mask and bbox data type
    Note 2 : new background image type must be one of .jpg, .jpeg, .png, .tif, .tiff, .PNG, .JPG, .JPEG, .TIF, .TIFF
    Args:
        background_dir_path (``Union[str, Path]``): Path to background folder
        p (``float``, **optional**): Probability. Defaults to 0.5.
    """

    IMPLEMENTED_TVTENSOR = [
        BoundingBoxes,
        Mask,
    ]  # list of available hooks, i.e implemented for these type of tv_tensor

    IMG_TYPE = [
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
        ".PNG",
        ".JPG",
        ".JPEG",
        ".TIF",
        ".TIFF",
    ]

    def __init__(self, background_dir_path: Union[str, Path], p: float = 0.5, **kwargs):

        super().__init__(**kwargs)
        path = (
            background_dir_path
            if isinstance(background_dir_path, Path)
            else Path(background_dir_path)
        )
        list_bckg_imgs = []
        for stem in RandomChangeBackground.IMG_TYPE:
            list_bckg_imgs += list(path.glob(f"*{stem}"))
        self.bckg_imgs = list_bckg_imgs
        self.p = p
        self._truth_extracter = _ExtractTruthFromTargetImage()

    def forward(self, *inputs):
        mu = torch.rand(1)
        if mu > self.p:
            return inputs
        assert (
            len(inputs) == 2
        ), f"RandomChangeBackground is implemented only for exactly image and target input provided. You can't provide only image or additional item like scores. Got {inputs}"
        image, target = inputs
        assert (
            type(target) in RandomChangeBackground.IMPLEMENTED_TVTENSOR
        ), f"RandomChangeBackground is implemented only for {RandomChangeBackground.IMPLEMENTED_TVTENSOR} torchvision tv_tensors. Got {type(target)}"

        # randomly select background image
        original_dtype = image.dtype
        image = image.float()
        idx = torch.randint(0, len(self.bckg_imgs), (1,)).item()
        bck_img = load_image(self.bckg_imgs[idx]).to(image.device).float()
        bck_img = T.Resize(image.shape[-2:])(bck_img)
        removed_bckg = self._truth_extracter(image, target)
        removed_bckg[removed_bckg == -1.0] = bck_img[removed_bckg == -1.0]
        return removed_bckg.to(original_dtype), target


class _ExtractTruthFromTargetImage:
    """Handle background removing from target. Background is asserted as -1 to avoid errors removing 0 entries from image."""

    def __call__(self, image: Tensor, targ: Tensor) -> Tensor:
        if isinstance(targ, Mask):
            rm_bckg = self._call_mask(image, targ)
        elif isinstance(targ, BoundingBoxes):
            rm_bckg = self._call_bbox(image, targ)
        return rm_bckg

    def _call_mask(self, image: Tensor, targ: Mask) -> Tensor:
        removed_bckg = copy.deepcopy(image)
        removed_bckg[:, targ == 0] = -1.0
        return removed_bckg

    def _call_bbox(self, image: Tensor, targ: BoundingBoxes) -> Tensor:
        mask = Mask(torch.zeros(image.shape[-2:]))
        for box in targ:
            x1, y1, x2, y2 = box.to(torch.uint64).split(1)
            x1, y1, x2, y2 = tuple(
                max(i.item(), 0) for i in (x1, y1, x2, y2)
            )  # ensure that bbox has coordinates positive
            mask[y1:y2, x1:x2] = 1
        return self._call_mask(image, mask)
