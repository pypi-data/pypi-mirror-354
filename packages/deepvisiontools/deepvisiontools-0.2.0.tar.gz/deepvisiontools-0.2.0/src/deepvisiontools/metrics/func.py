import torch
from torch import Tensor


# functionnals metrics
def f1score(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    for t in [tp,fp,tn,fn]:
        assert torch.is_tensor(t), "argument must be a tensor"
    return (2 * tp) / (2 * tp + fp + fn)


def precision(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    for t in [tp,fp,tn,fn]:
        assert torch.is_tensor(t), "argument must be a tensor"
    return (tp) / (tp + fp)


def recall(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    for t in [tp,fp,tn,fn]:
        assert torch.is_tensor(t), "argument must be a tensor"
    return (tp) / (tp + fn)


def iou(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    """Compute IoU from statistics."""
    for t in [tp,fp,tn,fn]:
        assert torch.is_tensor(t), "argument must be a tensor"
    return tp / (tp + fp + fn)


def accuracy(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    """Compute accuracy from statistics. In case of detection, tn is nan : -> 0 for computation"""
    for t in [tp,fp,tn,fn]:
        assert torch.is_tensor(t), "argument must be a tensor"
    tn[tn != tn] = 0 # set all NaN to 0 in tn
    return (tp + tn) / (tn + tp + fp + fn)
