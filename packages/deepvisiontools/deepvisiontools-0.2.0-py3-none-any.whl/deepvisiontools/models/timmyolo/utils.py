from torch import Tensor
from torchvision.transforms.v2.functional import crop
from typing import Tuple, List
import torch


class Patcher:
    def __init__(self, patch_size, overlap):
        self.patch_size = patch_size
        if isinstance(overlap, int) or isinstance(overlap, tuple):
            self.overlap = (overlap, overlap)
        else:
            self.overlap = (p * overlap for p in self.patch_size)

    def __call__(self, image, original_image_size):
        patchs, positions = self.patch_image(image, original_image_size)
        return patchs, positions

    def patch_image(self, images, original_img_size):
        patchs = []
        positions = []
        h_pos, w_pos = 0, 0
        while h_pos < original_img_size[0]:
            while w_pos < original_img_size[1]:
                positions.append((h_pos, w_pos, *self.patch_size))
                w_pos += int(self.patch_size[1] - self.overlap[1])
            h_pos += int(self.patch_size[0] - self.overlap[0])
            w_pos = 0
        for pos in positions:
            patchs.append(crop(images, *pos))

        return patchs, positions

    # def crop_img(self, image, positions: List[Tuple]):
    #     patchs = []
    #     for pos in positions:
    #         patchs.append(crop(image, *pos))
    #     return patchs

    def gen_pad_requirements(self, img_shape: torch.Size) -> Tuple[int, int, int, int]:
        last_pos = None
        h_pos, w_pos = 0, 0
        while h_pos < img_shape[-2]:
            while w_pos < img_shape[-1]:
                last_pos = (h_pos, w_pos, *self.patch_size)
                w_pos += int(self.patch_size[1] - self.overlap[1])
            h_pos += int(self.patch_size[0] - self.overlap[0])
            w_pos = 0
        target_H, target_W = last_pos[0] + last_pos[2], last_pos[1] + last_pos[3]
        t_pad = int((target_H - img_shape[0]) / 2.0)
        b_pad = target_H - img_shape[0] - t_pad
        l_pad = int((target_W - img_shape[1]) / 2.0)
        r_pad = target_W - img_shape[1] - l_pad
        return l_pad, t_pad, r_pad, b_pad


class PatchLoader:
    """Wrap predictor patchification output as loader with given batch_size for forward"""

    def __init__(self, patches: Tensor, batch_size: int = 1):
        N_ = patches.shape[0]
        batchs = []
        for i in range(N_ // batch_size + 1):
            if i * batch_size >= N_:
                break
            if (i + 1) * batch_size < N_:
                batchs.append(patches[i * batch_size : (i + 1) * batch_size])
            else:
                batchs.append(patches[i * batch_size :])
                break
        self.batchs = batchs

    def __iter__(self):
        return iter(self.batchs)

    def __len__(self):
        return len(self.batchs)


def avg_stack(feats1: Tensor, feats2: Tensor) -> Tuple[Tensor]:
    combined_logits = torch.stack([feats1, feats2])  # (2, C, H, W)
    # apply mean on logits
    combined_logits = torch.mean(combined_logits.float(), dim=0)  # (C, H, W)
    return combined_logits


def combine_features(
    feat1: Tensor, feat2: Tensor, weight1: Tensor, weight2: Tensor
) -> Tuple[Tensor]:
    """fuse features

    Args:
        logit1 (``Tensor``)
        logit2 (``Tensor``)

    Returns:
        ``Tuple[Tensor]``
    """
    assert (
        feat1.shape == feat2.shape
    ), f"Can't aggregate logits of differents shape. Got {feat1.shape} and {feat2.shape}"
    func = avg_stack
    new_feat = torch.zeros(feat1.shape).to(feat1.device)
    # mask of intersected non zero masks
    intersected_non_0_mask = torch.logical_and(feat1 != 0, feat2 != 0)
    intersected_oneis0_mask = torch.logical_xor(feat1 != 0, feat2 != 0)
    # if both are non 0 then use the appropriate aggregation strategy
    new_feat[intersected_non_0_mask] = func(
        feat1[intersected_non_0_mask], feat2[intersected_non_0_mask]
    )
    # take the max if one of them is 0
    new_feat[intersected_oneis0_mask] = torch.max(torch.stack([feat1, feat2]), dim=0)[
        0
    ][intersected_oneis0_mask]
    return new_feat


def normalize_boxes(boxes: Tensor, img_size: Tuple[int, int]) -> Tensor:
    """Normalize boxes to 1 -> h, w -> [0, 1] according to img size

    Args:
        boxes (``Tensor``): boxes Tensor
        img_size (``Tuple[int, int]``): image size

    Returns:
        ``Tensor``:
            - normalized boxes
    """
    boxes = boxes.float()
    image_w = img_size[1]
    image_h = img_size[0]
    boxes[:, 0] = boxes[:, 0] / image_w
    boxes[:, 1] = boxes[:, 1] / image_h
    boxes[:, 2] = boxes[:, 2] / image_w
    boxes[:, 3] = boxes[:, 3] / image_h
    return boxes


from deepvisiontools.formats import BaseFormat
from deepvisiontools import Configuration
from math import ceil, floor
from typing import Tuple
from torchvision.ops import nms
from torch import Tensor


def yolo_pad_requirements(h: int, w: int, required=32) -> Tuple[int, int, int, int]:
    """Conmpute pad coordinates to ensure /32 or /64 yolo criterium on height and width

    Args:
        h (``int``): height
        w (``int``): width
    Returns:
        ``Tuple[int, int, int, int]``:
            - top, left, right, bottom
    """
    diff_h, diff_w = h % required, w % required
    pad_h = required - diff_h if diff_h > 0 else 0
    pad_w = required - diff_w if diff_w > 0 else 0
    # define padding for each border
    if pad_h or pad_w:
        half_h, half_w = pad_h / 2, pad_w / 2
        left, top, right, bottom = (
            ceil(half_w),
            ceil(half_h),
            floor(half_w),
            floor(half_h),
        )
    else:
        left, top, right, bottom = (0, 0, 0, 0)
    return (top, left, right, bottom)


def confidence_filter(format: BaseFormat) -> BaseFormat:
    """Filter Format according to confidence threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    assert format.scores != None, "Scores are not in format: cannot filter."
    new_format, _ = format[format.scores > Configuration().model_confidence_threshold]
    return new_format


def box_nms_filter(format: BaseFormat) -> BaseFormat:
    """Filter Format according to nms threshold from Configuration()

    Args:
        format (``Format``)

    Returns:
        ``Format``
    """
    if format.nb_object == 0:
        return format
    original_format = format.data.format
    format.data.format = "XYXY"
    indexes: Tensor = nms(
        format.data.value.float(),
        scores=format.scores.float(),
        iou_threshold=Configuration().model_nms_threshold,
    )
    indexes = indexes.to(Configuration().device).sort()[0]
    format.data.format = original_format
    new_format, _ = format[indexes]
    return new_format


def normalize_boxes(boxes: Tensor, img_size: Tuple[int, int]) -> Tensor:
    """Normalize boxes to 1 -> h, w -> [0, 1] according to img size

    Args:
        boxes (``Tensor``): boxes Tensor
        img_size (``Tuple[int, int]``): image size

    Returns:
        ``Tensor``:
            - normalized boxes
    """
    boxes = boxes.float()
    image_w = img_size[1]
    image_h = img_size[0]
    boxes[:, 0] = boxes[:, 0] / image_w
    boxes[:, 1] = boxes[:, 1] / image_h
    boxes[:, 2] = boxes[:, 2] / image_w
    boxes[:, 3] = boxes[:, 3] / image_h
    return boxes
