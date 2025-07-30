from __future__ import annotations
from typing import Tuple
from torch import Tensor
from deepvisiontools.formats.base_data import (
    InstanceMaskData,
    BboxData,
    SemanticMaskData,
)
from deepvisiontools.formats.base_formats import BaseFormat, BaseSemanticFormat
import torch
import deepvisiontools.formats.errors as er
from typing import Union, List, Literal
from deepvisiontools import Configuration
import copy


class SemanticMaskFormat(BaseSemanticFormat):
    """Class for Semantic Mask format (Child class of *BaseSemanticFormat*).

    Args:
        data (SemanticMaskData)
        scores (Tensor | None, optional). Defaults to None.

    Properties & attributes : cf *BaseSemanticFormat*


    **Methods**
    """

    @classmethod
    def from_instance_mask(
        cls, mask: InstanceMaskFormat, scores: Tensor | None = None
    ) -> BboxFormat:
        """Create a SemanticMaskFormat from InstanceMaskFormat

        Args:
            mask (InstanceMaskFormat)

        Returns:
            SemanticMaskFormat
        """
        semanticmask = SemanticMaskData(mask.export_semantic_mask())
        return SemanticMaskFormat(semanticmask, scores=None)

    @classmethod
    def empty(cls, canvas_size: Tuple[int], scores: Tensor | None = None) -> BboxFormat:
        """Create an empty SemanticMaskFormat of dimension canvas_size

        Args:
            canvas_size (Tuple[int, int])

        Returns:
            SemanticMaskFormat
        """
        return SemanticMaskFormat(SemanticMaskData.empty(canvas_size), scores=scores)

    def __init__(self, data: SemanticMaskData, scores: Tensor | None = None):
        assert isinstance(
            data, SemanticMaskData
        ), f"Expect to have SemanticMaskData data for SemanticMaskFormat, got {type(data)}."
        super().__init__(data, scores)

    def generate_scores_from_mask(self):
        if Configuration().num_classes == 1:
            scores = copy.deepcopy(self.data.value)[None, :]
        else:
            scores = copy.deepcopy(self.data.value)
            scores = (
                torch.nn.functional.one_hot(scores, Configuration().num_classes)
                .float()
                .permute(2, 0, 1)
            )  # These are perfects logits
        return SemanticMaskFormat(self.data, scores=scores)


class InstanceMaskFormat(BaseFormat):
    """Class for Instance Segmentation Format (Child class of *BaseFormat*). contains *InstanceMaskData* value, labels and scores.

    Args:
        data (InstanceMaskData)
        labels (Tensor)
        scores (Tensor | None, optional). Defaults to None.

    Properties & attributes : cf *BaseFormat*


    **Methods**
    """

    @classmethod
    def empty(cls, canvas_size: Tuple[int, int]) -> InstanceMaskFormat:
        """Create an empty InstanceMaskFormat of dimension canvas_size

        Args:
            canvas_size (Tuple[int, int])

        Returns:
            InstanceMaskFormat
        """
        return InstanceMaskFormat(
            InstanceMaskData.empty(canvas_size), labels=torch.tensor([])
        )

    def __init__(
        self, data: InstanceMaskData, labels: Tensor, scores: Tensor | None = None
    ):

        assert isinstance(
            data, InstanceMaskData
        ), f"Expect to have InstanceMaskData data for InstanceMaskFormat, got {type(data)}."
        super().__init__(data, labels, scores)

    def export_semantic_mask(self) -> Tensor:
        """From self (data.value and labels) generate a semantic mask by replacing objects indexing by their corresponding labels.
        Note that labels are shifted by 1 as 0 is preserved for background

        Returns:
            ``Tensor``:
                - Semantic mask
        """
        inst_mask, _ = self.sanitize()
        semantic_mask = torch.zeros(self.canvas_size).to(self.device)
        semantic_mask = semantic_mask.long()
        if self.nb_object == 0:
            return semantic_mask
        for i, lab in enumerate(self.labels):
            semantic_mask[inst_mask.data.value == (i + 1)] = lab.item() + 1
        return semantic_mask


class BboxFormat(BaseFormat):
    """Class for Bounding box format (Child class of *BaseFormat*). contains *BBoxData* value, labels and scores.

    Args:
        data (BBoxData)
        labels (Tensor)
        scores (Tensor | None, optional). Defaults to None.

    Properties & attributes : cf *BaseFormat*


    **Methods**
    """

    @classmethod
    def from_instance_mask(cls, mask: InstanceMaskFormat) -> BboxFormat:
        """Create a BboxFormat from InstanceMaskFormat

        Args:
            mask (InstanceMaskFormat)

        Returns:
            BboxFormat
        """
        mask, _ = mask.sanitize()
        boxes = BboxFormat(BboxData.from_mask(mask.data), mask.labels, mask.scores)
        assert (
            mask.nb_object == boxes.nb_object
        ), "Different number of objects when creating boxes from instance masks, you may need to increase the mask_min_size parameter in Configuration()"
        return boxes

    @classmethod
    def empty(cls, canvas_size: Tuple[int]) -> BboxFormat:
        """Create an empty BboxFormat of dimension canvas_size

        Args:
            canvas_size (Tuple[int, int])

        Returns:
            BboxFormat
        """
        return BboxFormat(BboxData.empty(canvas_size), labels=torch.tensor([]))

    def __init__(self, data: BboxData, labels: Tensor, scores: Tensor | None = None):
        assert isinstance(
            data, BboxData
        ), f"Expect to have BboxData data for BboxFormat, got {type(data)}."
        super().__init__(data, labels, scores)


class BatchedFormat:
    """A class that handles a list of Formats

    Args:
        formats (``List[BaseFormat]``)

    Attributes
    ----------

    Properties:
        - device (``Literal[&quot;cpu&quot;, &quot;cuda&quot;]``): When changed, move all formats into same device.
        - formats (``List[BaseFormat]``): contains all stored formats.
        - size (``int``): number of formats


    **Methods**
    """

    @classmethod
    def cat(self, batches: List[BatchedFormat]):
        """batches need to be a list of BatchedFormat of same type !"""
        new_list = []
        for batch in batches:
            new_list += batch.formats
        return BatchedFormat(new_list)

    def __init__(self, formats: List[BaseFormat]):

        formats_check = [isinstance(form, BaseFormat) for form in formats]
        assert all(
            formats_check
        ), f"Some targets are not Format, got {[type(form) for form in formats]}"
        self.formats: List[BaseFormat] = formats
        self.sanitize()

    def sanitize(self):
        """Apply sanitize to all formats"""
        self.formats = [form.sanitize()[0] for form in self.formats]

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, val: List[BaseFormat]):
        self._canvas_size = val[0].canvas_size if len(val) != 0 else None
        self._formats = val
        self._size = len(val)
        self.device = Configuration().device

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val):
        for form in self.formats:
            form.device = val
        self._device = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        raise er.ProtectedAttributeException()

    def __getitem__(self, indexes: Union[int, slice, Tensor]) -> BatchedFormat:
        if isinstance(indexes, Tensor):
            if indexes.dtype == torch.bool:
                indexes = indexes.cpu().tolist()
                indexes = [i for i, val in enumerate(indexes) if val]
            else:
                indexes = indexes.cpu().tolist()
                indexes = [i in indexes for i in range(len(indexes))]
        if isinstance(indexes, list):
            new_batch = [self.formats[i] for i in indexes]
        else:
            new_batch = self.formats[indexes]
        if not isinstance(new_batch, list):
            new_batch = [new_batch]
        return BatchedFormat(
            new_batch
        )  # TODO : this has been modified, originally it was only the list ... It must be checked intensivelly !!!

    def set_bboxes_format(self, val: Literal["XYXY", "XYWH", "CXCYWH"]):
        for form in self.formats:
            assert isinstance(
                form, BboxFormat
            ), f"In BatchedFormat: can't change bbox format of object {type(form)}"
            form.data.format = val

    def __next__(self):
        _next: BaseFormat = next(self.__iter__())
        return _next

    def __iter__(self):
        return iter(self.formats)

    def __add__(self, form2: BatchedFormat):
        return BatchedFormat(self.formats + form2.formats)
