import segmentation_models_pytorch as smp
from deepvisiontools.models.basemodel import BaseModel
from typing import Literal, Union, Tuple
import torch
from torch import Tensor
from deepvisiontools.config import Configuration
import deepvisiontools.models.smp.errors as er
import inspect
from segmentation_models_pytorch.base.model import SegmentationModel
from deepvisiontools.formats import SemanticMaskFormat, SemanticMaskData, BatchedFormat
import copy
from deepvisiontools.formats.utils import logit2pred


class _ConcreteSegmentationModel(BaseModel):
    """Concrete implementation of deepvisiontools BaseModel used for SMP models.
    This is used as one of the two parent class of dynamically created class _SMP"""

    def __init__(self, *args, **kwargs):
        mode = "binary" if Configuration().num_classes == 1 else "multiclass"
        loss = kwargs.pop("loss", smp.losses.FocalLoss(mode=mode))
        super().__init__(*args, **kwargs)
        assert (
            loss.mode == mode
        ), f"Loss has inconsistent mode (multiclass or binary) compared to num_classes. Got {loss.mode} and {Configuration().num_classes}"
        self.loss = loss

    def prepare(self, images, targets=None):
        targets = torch.stack([targ.data.value for targ in targets])
        return images, targets

    def run_forward(self, images, targets):
        images, batched_targets = self.prepare(images, targets)
        logits = self.activation(self(images))
        loss_dict = {"loss": self.loss(logits, batched_targets)}
        if self.training:
            return loss_dict
        else:
            return loss_dict, self.build_results(logits)

    def build_results(self, raw_outputs):
        raw_outputs = (
            raw_outputs if raw_outputs.ndim == 4 else raw_outputs[None, :]
        )  # raw outputs are logits
        logits = copy.deepcopy(raw_outputs)
        # Transform logits to preds (2 cases : binary vs multiclass). needs to handle batch size as well
        preds = torch.stack([logit2pred(l) for l in logits])
        # convert preds to BatchedFormat
        preds = [SemanticMaskData(t) for t in preds]
        preds = [SemanticMaskFormat(f, scores=l) for f, l in zip(preds, logits)]
        preds = BatchedFormat(preds)
        return preds

    def get_predictions(self, images):
        self.eval()
        logits = self.activation(self(images))
        preds = self.build_results(logits)
        return preds

    def activation(self, prediction: Tensor):
        """Return activated predictions by sigmoid (single class) of softmax (multi class).

        Args:
            prediction (Tensor): Raw model ouput/raw probabilities.
        """
        num_classes = Configuration().num_classes
        prediction_dims = prediction.ndim
        assert prediction_dims in [
            3,
            4,
        ], f"Number of dimension in prediction should be 3 or 4 (batch), got {prediction_dims}"
        channel = 0 if prediction_dims == 3 else 1
        if num_classes == 1:
            prediction = prediction.sigmoid()
        elif num_classes > 1:
            prediction = prediction.softmax(dim=channel)  # Channels dimension

        return prediction


class SMP(torch.nn.Module):
    """Factory class that wraps segmentation-models-pytorch (smp) models into deepvisiontools. These models are used for semantic segmentation tasks.
    Using this class you can use all available models, encoder and whatever additional arguments from segmentation model pytorch. Please provide further parameters using non positional arguments (ex : arg=myadditionalarg)
    Note that you can use any smp loss as well by simply providing and instance of smp losses : loss=smp.loss.WantedLoss()

    smp : https://github.com/qubvel-org/segmentation_models.pytorch

    Args:
        architecture (``SegmentationModel``, **optional**): SMP model architecture : need to provide a smp class (type). Defaults to smp.Unet.

    Example:
    ----------

    .. highlight:: python
    .. code-block:: python

        >>> from deepvisiontools.models import SMP
        >>> import segmentation_models_pytorch as smp
        >>> my_model = SMP(smp.Unet, encoder_name="vgg11", loss=smp.losses.FocalLoss(mode="binary"))
    """

    def __new__(cls, architecture: SegmentationModel = smp.Unet, *args, **kwargs):

        assert (
            Configuration().data_type == "semantic_mask"
        ), f"Can't use SMP models (used for semantic segmentation) if Configuration().data_type is not semantic_mask. Got {Configuration().data_type}."

        num_cls = Configuration().num_classes

        # to avoid errors if architecture is smp.Unet or smp.Unet(), ensure that we have a type and not and instance
        architecture = (
            architecture if isinstance(architecture, type) else type(architecture)
        )

        # Get class number and feed to kwargs
        kwargs["classes"] = num_cls

        # Dynamically create class
        class _SMP(_ConcreteSegmentationModel, architecture):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.init_args = args
                self.architecture = architecture
                self.init_kwargs = kwargs

            def __reduce__(self):
                # used by pickle in torch.save
                return (
                    SMP._rebuild_model,
                    (
                        self.architecture,
                        self.init_args,
                        self.init_kwargs,
                        self.state_dict(),
                    ),
                )

        instance = _SMP(*args, **kwargs)
        # return newly created instance from dynamically inheritated smp class
        return instance

    @staticmethod
    def _rebuild_model(architecture, args, kwargs, state_dict):
        kwargs["encoder_weights"] = (
            None  # Not downloading pretrained weights when using torch.load
        )
        model = SMP(architecture, *args, **kwargs)
        model.load_state_dict(state_dict)
        return model
