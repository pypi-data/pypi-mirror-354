from torch import Tensor
from pathlib import Path
import torch
from typing import Union
from PIL import Image
import torchvision.transforms.functional as F
from torchvision.transforms.functional import pil_to_tensor
import warnings


def save_image(image: Union[Tensor, Image.Image], path: Union[str, Path]) -> Image:
    """Transform image in PIL format and save to given path."""
    if not isinstance(path, Path):
        path = Path(path)
    parent = path.parent
    Path(parent).mkdir(exist_ok=True, parents=True)
    if isinstance(image, Image.Image):
        image.save(path.as_posix())
    else:
        image = image.to(torch.uint8)
        pil_image = F.to_pil_image(image)
        pil_image.save(path.as_posix())


def save_mask(mask: Union[Tensor, Image.Image], path: Union[str, Path]) -> Image:
    """Transform mask in PIL format and save to given path."""
    if not isinstance(path, Path):
        path = Path(path)
    parent = path.parent
    if not parent.exists():
        Path(parent).mkdir(exist_ok=True, parents=True)
    if isinstance(mask, Image.Image):
        mask.save(path.as_posix())
    else:
        assert isinstance(
            mask, Tensor
        ), f"Mask must be either pil.Image object or Tensor, got {type(mask)}"
        if not path.suffix in [".tiff", ".TIFF"]:
            warnings.warn(
                "file type for mask is not tif, deepvisiontools will change it for tif (annotation masks must support long / float to avoid issues for large class numbers)"
            )
            path = (path.parent / path.stem).with_suffix(".tiff")
        mask = mask.float()
        pil_image = Image.fromarray(mask.detach().numpy())
        pil_image.save(path.as_posix())


def load_image(image_path: Union[str, Path]) -> Tensor:
    """Load image using torchvision. Handles png, tiff, jpg, jpeg extensions.

    Args:
        image_path (str): Path to image.

    Returns:
        Tensor: image in torch Tensor [3, H, W].
    """
    if isinstance(image_path, str):
        image_path = Path(image_path)
    img = Image.open(image_path)
    img = pil_to_tensor(img)
    return img


def load_mask(mask_path: Union[str, Path]) -> Tensor:
    """Load image using torchvision. Handles png, tiff, jpg, jpeg extensions.

    Args:
        image_path (str): Path to image.

    Returns:
        Tensor: image in torch Tensor [3, H, W].
    """
    if isinstance(mask_path, str):
        mask_path = Path(mask_path)
    img = Image.open(mask_path)
    img = pil_to_tensor(img)
    assert img.shape[0] == 1, f"Mask must have only one channel, got {img.shape[0]}"
    img = img.long()[0]
    return img
