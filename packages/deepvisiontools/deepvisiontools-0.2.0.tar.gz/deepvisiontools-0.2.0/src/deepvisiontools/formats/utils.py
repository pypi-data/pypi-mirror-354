import torch
from torch import Tensor
from torchvision.ops import masks_to_boxes
import copy
import cv2
import numpy as np
from typing import Tuple
from deepvisiontools import Configuration
import copy


def mask2boxes(mask: Tensor) -> Tensor:
    """from stacked (id object = 1 ... N) mask (H, W) returns tensor of shape (N, 4)"""
    assert (
        mask.dim() == 2
    ), f"mask must be a stacked (id object = 1 ... N) mask of shape (H, W), got {mask.shape}"
    if torch.max(mask) == 0:
        return torch.empty((0, 4)).to(mask.device)
    objs = torch.arange(1, torch.max(mask) + 1)
    box_list = []
    for i in objs:
        m = copy.deepcopy(mask)
        m[mask != i] = 0
        m[mask == i] = 1
        box_list.append(masks_to_boxes(m[None, :]))
    return torch.cat(box_list, dim=0)


def reindex_mask_with_splitted_objects(mask: Tensor) -> Tuple[Tensor, Tensor]:
    """Function that reidex masks objects by creating new objects if they are disconnected.

    Args:
        mask (``Tensor``): Input mask tensor containing disconnected part of given objects.

    Returns:
        ``Tuple[Tensor, Tensor]``:
            - New mask indexed with 1 per object after separating disconnected objects, indexes of original common objects they belonged.

    Detailed explanation : Imagine a mask with 2 objects 0 and 1 and the first is separated in two parts disconnected.
    The new mask will contain 3 objects and the indices will be [0, 0, 1]

    """
    assert (
        mask.dim() == 2
    ), f"mask must be a stacked (id object = 1 ... N) mask of shape (H, W), got {mask.shape}"
    if torch.max(mask) == 0:
        return mask, torch.tensor([])

    objs = torch.arange(1, torch.max(mask) + 1)
    new_mask = torch.zeros(mask.shape).to(mask.device)
    split_count = 0
    new_labels_indices = []
    for i in objs:
        m = copy.deepcopy(mask)
        m[mask != i] = 0
        m[mask == i] = i
        np_mat = m.detach().cpu().numpy().astype(np.uint8)
        bool_mat = np_mat == 0
        contours, _ = cv2.findContours(
            np_mat,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE,
        )
        mat = np.zeros(np_mat.shape)
        for j, c in enumerate(contours):
            split_count += j
            val = float(i + split_count)
            cv2.fillConvexPoly(mat, c, (val, val, val))
            new_labels_indices.append(i)
        mat[bool_mat] = 0
        add_mask = torch.tensor(mat).to(mask.device)
        new_mask, _ = torch.max(torch.stack([new_mask, add_mask]), dim=0)
    return new_mask, torch.tensor(new_labels_indices).to(new_mask.device)


# ============= Handling logits combination for add method in semantic mask formats ===============

# TODO check binary vs multiclass


def avg_stack(
    logit1: Tensor,
    logit2: Tensor,
) -> Tuple[Tensor]:
    combined_logits = torch.stack([logit1, logit2])  # (2, N_cls, H, W)
    # apply mean on logits
    combined_logits = torch.mean(combined_logits.float(), dim=0)  # (N_cls, H, W)
    return combined_logits


def min_stack(
    logit1: Tensor,
    logit2: Tensor,
) -> Tuple[Tensor]:
    combined_logits = torch.stack([logit1, logit2])  # (2, N_cls, H, W)
    # apply mean on logits
    combined_logits = torch.min(combined_logits, dim=0)  # (N_cls, H, W)
    return combined_logits


def max_stack(
    logit1: Tensor,
    logit2: Tensor,
) -> Tuple[Tensor]:
    combined_logits = torch.stack([logit1, logit2])  # (2, N_cls, H, W)
    # apply mean on logits
    combined_logits = torch.min(combined_logits, dim=0)  # (N_cls, H, W)
    return combined_logits


OPERATORS_FUNCTIONS = {
    "avg": avg_stack,
    "min": min_stack,
    "max": max_stack,
}


def logit2pred(logit):
    """transform logits into pred"""
    # Transform logits to preds (2 cases : binary vs multiclass)
    log = copy.deepcopy(logit)
    if Configuration().num_classes == 1:
        preds = log
        preds[preds >= 0.5] = 1
        preds[preds < 0.5] = 0
    else:
        preds = torch.argmax(log, dim=0)
    return preds


# TODO Handle aggregation strategies including for patchification
def combine_logits(
    logit1: Tensor,
    logit2: Tensor,
) -> Tuple[Tensor]:
    """Used for semantic mask data, and particularly in patchification.
    Take 2 logits mask and combine them according to Configuration().semantic_mask_logits_combination
    If one mask has strictly zeros somewhere, just take the other value. If both are zeros become zeros. If both are non zeros, combine them.

    Args:
        logit1 (``Tensor``)
        logit2 (``Tensor``)

    Returns:
        ``Tuple[Tensor]``
    """
    assert (
        logit1.shape == logit2.shape
    ), f"Can't aggregate logits of differents shape. Got {logit1.shape} and {logit2.shape}"
    func = OPERATORS_FUNCTIONS[Configuration().semantic_mask_logits_combination]
    new_logit = torch.zeros(logit1.shape).to(logit1.device)
    # mask of intersected non zero masks
    intersected_non_0_mask = torch.logical_and(logit1 != 0, logit2 != 0)
    intersected_oneis0_mask = torch.logical_xor(logit1 != 0, logit2 != 0)
    # if both are non 0 then use the appropriate aggregation strategy
    new_logit[intersected_non_0_mask] = func(
        logit1[intersected_non_0_mask], logit2[intersected_non_0_mask]
    )
    # take the max if one of them is 0
    new_logit[intersected_oneis0_mask] = torch.max(
        torch.stack([logit1, logit2]), dim=0
    )[0][intersected_oneis0_mask]
    return new_logit


def get_preds_and_logits(
    logit1: Tensor,
    logit2: Tensor,
) -> Tuple[Tensor]:
    """Combine 2 logits (used in __add__ of semanticmaskformat) and return semantic mask and logits"""
    assert logit1.shape == logit2.shape, "logits must have same shape to be combined"
    combined_logits = combine_logits(logit1, logit2)  # (N_cls, H, W)
    semantic_mask = logit2pred(combined_logits)  # Semantic mask with (H, W)
    return semantic_mask, combined_logits
