from __future__ import annotations
from deepvisiontools.formats.base_data import BaseData, SemanticMaskData
from typing import Literal, Union, Tuple
import deepvisiontools.formats.errors as er
from torch import Tensor
import torch
from abc import ABC, abstractmethod
from torchvision.transforms.v2 import Transform
import deepvisiontools.formats.utils as ut
from torchvision.tv_tensors import Mask


class BaseFormat(ABC):
    """Base class to wrap BaseData (masks, boxes and others elements) of targets / predictions with labels and scores in deepvisiontools.

    Args:
        data (BaseData)
        labels (Tensor)
        scores (Union[Tensor, None], optional): Defaults to None.

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``): When changed, move data, labels and scores stored into same device.
        - data (``BaseData``): value of data like InstanceMaskData, BboxData etc.
        - scores (``Union[Tensor, None]``): scores as a 1d tensor.
        - labels (``Tensor``): labels as a 1d tensor.
        - nb_object (``int``): number of objects
        - canvas_size (``Tuple[int, int]``): Size of associated image (h, w)


    **Methods**:
    """

    @abstractmethod
    def empty(canvas_size: Tuple[int, int]):
        pass

    @abstractmethod
    def __init__(
        self, data: BaseData, labels: Tensor, scores: Union[Tensor, None] = None
    ):
        self._data = data
        # labels is always present, scores can be None
        self._labels: Tensor = labels.long()
        self._scores: Union[Tensor, None] = scores
        # Check sanity of initialized attributes
        self._canvas_size = data.canvas_size
        er.check_format_init("labels", self, Tensor)
        if self.scores != None:
            er.check_format_init("scores", self, Tensor)
        self._nb_object = self.labels.nelement()
        er.check_labels_size(self)
        # define the operator handler
        self._ops = FormatOperatorHandler()
        self.device = data.device

    @property
    def data(self) -> BaseData:
        return self._data

    @data.setter
    def data(self, val):
        raise er.ProtectedAttributeException()

    @property
    def canvas_size(self):
        return self._canvas_size

    @canvas_size.setter
    def canvas_size(self, val):
        raise er.ProtectedAttributeException()

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val: Literal["cpu", "cuda"]):
        self.data.device = val
        self._labels = self._labels.to(val)
        if self.scores != None:
            self._scores = self._scores.to(val)
        self._device = val

    @property
    def nb_object(self):
        return self._nb_object

    @nb_object.setter
    def nb_object(self, val):
        raise er.ProtectedAttributeException()

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, val):
        raise er.ProtectedAttributeException()

    @property
    def scores(self):
        return self._scores

    @scores.setter
    def scores(self, val):
        raise er.ProtectedAttributeException()

    def crop(self, t: int, l: int, h: int, w: int) -> Tuple[BaseFormat, Tensor]:
        new_format, present = self._ops.apply_base_method(
            self, "crop", t=t, l=l, h=h, w=w
        )
        return new_format, present

    def pad(self, t, l, r, b) -> Tuple[BaseFormat, Tensor]:
        new_format, present = self._ops.apply_base_method(
            self, "pad", t=t, l=l, r=r, b=b
        )
        return new_format, present

    def pad_to(self, new_size):
        new_h, new_w = new_size
        t = int((new_h - self.canvas_size[0]) / 2)
        l = int((new_w - self.canvas_size[1]) / 2)
        r = int((new_w - self.canvas_size[1]) - l)
        b = int((new_h - self.canvas_size[0]) - t)
        assert t >= 0 and l >= 0, f"Cannot pad {self.canvas_size} to {new_size}"
        new_format, present = self.pad(t, l, r, b)
        return new_format, present

    def sanitize(self) -> Tuple[BaseFormat, Tensor]:
        """Sanitize the format.

        Returns:
            Tuple[BaseFormat, Tensor]: sanitized Format, indices of present objects
        """
        new_format, present = self._ops.apply_base_method(self, "sanitize")
        return new_format, present

    def __getitem__(self, indexes: Union[int, slice, Tensor]):
        new_format, present = self._ops.apply_base_method(
            self, "__getitem__", indexes=indexes
        )
        return new_format, present

    def __add__(self, obj2: BaseFormat) -> BaseFormat:
        """Add 2 formats of same nature together (add objects). NB : In case of InstanceMaskFormat which handles stacked masks, this will remove overlapping mask information (replaced by second object)."""
        assert isinstance(
            obj2, type(self)
        ), f"Formats are not same type, cant add {type(self)} with {type(obj2)}."
        labels = torch.cat([self.labels, obj2.labels])
        if self.scores == None or obj2.scores == None:
            scores = None
        else:
            scores = torch.cat([self.scores, obj2.scores])
        data = self.data + obj2.data
        return type(self)(data, labels, scores)

    def apply_augmentation(
        self, image: Tensor, transform: Transform
    ) -> Tuple[BaseFormat, Tensor, Tensor]:
        """Apply augmentation. Handles labels as well and image.

        Args:
            form (``BaseFormat``)
            image (``Tensor``)
            transform (``Transform``)

        Returns:
            ``Tuple[BaseFormat, Tensor, Tensor]``:
                - augmented format, present Tensor, augmented image
        """
        return self._ops.apply_augmentation(self, image, transform)


class BaseSemanticFormat(BaseFormat):

    # overwrite
    def __init__(self, data: SemanticMaskData, scores: Tensor | None = None):
        assert isinstance(
            data, SemanticMaskData
        ), f"BaseSemanticFormat requires data to be SemanticMaskData object, got {type(data)}"
        if scores != None:
            assert (
                scores.ndim == 3
            ), f"Scores must be of dimension 3 or None, got {scores.shape}"
            assert (
                scores.shape[-2:] == data.value.shape[-2:]
            ), f"scores do not have the same shape as data.value, got {scores.shape} and {data.value.shape}"
        self._data = data
        # labels are derived from semantic mask data value (careful : need to handle the case where 0 is not present in mask ...)
        labs = (
            data.value.unique()[1:].long()
            if 0 in data.value.unique().tolist()
            else data.value.unique().long()
        )
        self._labels: Tensor = labs
        # Check score
        if scores != None:
            scores = (
                scores.float() if isinstance(scores, Mask) else Mask(scores.float())
            )
        self._scores: Union[Tensor, None] = scores
        # Check sanity of initialized attributes
        self._canvas_size = data.canvas_size
        self._nb_object = data.nb_object
        # define the operator handler
        self._ops = SemanticFormatOperatorHandler()
        self.device = data.device

    def __add__(self, obj: BaseSemanticFormat):
        new_obj = self._ops._apply_add_method(self, obj)
        return new_obj


class FormatOperatorHandler:
    """Class that handles operations on format such as crop, pad, sanitize etc.


    **Methods**:
    """

    def __init__(self):
        pass

    def redefine_labels_scores(self, labs: Tensor, present: Tensor):
        # redefin labels or scores according to presence of objects
        new = labs[present.tolist()]
        return new

    def apply_base_method(
        self, form: BaseFormat, func: str, **kwargs
    ) -> Tuple[BaseFormat, Tensor]:
        """Apply a base method (crop, pad, sanitize etc.) from BaseData and handles labels modifications.
        The method must return as well a present objects Tensor : [BaseData, Tensor]

        Args:
            func (``str``): func to be called (ex: crop, pad ...)

        Returns:
            ``Tuple[Format, Tensor]``:
                - New format and tensor of present objects after operation
        """

        new_data, present = getattr(form.data, func)(**kwargs)
        new_labels = self.redefine_labels_scores(form.labels, present)
        if form.scores != None:
            new_scores = self.redefine_labels_scores(form.scores, present)
        else:
            new_scores = None
        new_format = type(form)(new_data, new_labels, new_scores)
        return new_format, present

    def apply_augmentation(
        self, form: BaseFormat, image: Tensor, transform: Transform
    ) -> Tuple[BaseFormat, Tensor, Tensor]:
        """Apply augmentation on BaseData through its method. Handles labels as well and image.

        Args:
            form (``BaseFormat``)
            image (``Tensor``)
            transform (``Transform``)

        Returns:
            ``Tuple[BaseFormat, Tensor, Tensor]``:
                - augmented format, present Tensor, augmented image
        """
        augmented_data, present, augmented_image = form.data.apply_augmentation(
            image, transform
        )
        new_labels = self.redefine_labels_scores(form.labels, present)
        if form.scores != None:
            new_scores = self.redefine_labels_scores(form.scores, present)
        else:
            new_scores = None
        new_format = type(form)(augmented_data, new_labels, new_scores)
        return new_format, present, augmented_image


class SemanticFormatOperatorHandler(FormatOperatorHandler):

    def apply_augmentation(
        self, form: BaseSemanticFormat, image: Tensor, transform: Transform
    ) -> Tuple[BaseFormat, Tensor, Tensor]:

        if form.scores != None:
            augmented_data, present, augmented_image, augmented_scores = (
                form.data.apply_augmentation(image, transform, form.scores)
            )
        else:
            augmented_data, present, augmented_image = form.data.apply_augmentation(
                image, transform
            )
            augmented_scores = None

        return (
            type(form)(augmented_data, scores=augmented_scores),
            present,
            augmented_image,
        )

    def apply_base_method(self, form, func, **kwargs):
        if func != "__add__":
            return self._apply_base_method(form, func, **kwargs)
        else:
            return self._apply_add_method(form, **kwargs)

    def _apply_add_method(self, form: BaseSemanticFormat, form2: BaseSemanticFormat):
        assert (
            form.scores != None and form2.scores != None
        ), f"Cant't add 2 BaseSemanticFormat if their scores are None. Got {form.scores} and {form2.scores}"
        mask, scores = ut.get_preds_and_logits(form.scores, form2.scores)
        mask = SemanticMaskData(mask)
        mask = type(form)(mask, scores=scores)
        return mask

    def _apply_base_method(self, form: BaseSemanticFormat, func, **kwargs):
        if form.scores != None:
            form.data._scores = form.scores
        new_data, present = getattr(form.data, func)(**kwargs)
        new_scores = new_data._scores
        new_format = type(form)(new_data, new_scores)
        form.data._scores = None
        return new_format, present
