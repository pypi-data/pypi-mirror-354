import torch
import torch.nn as nn
import timm
from ultralytics.nn.modules.head import Detect, Segment
from deepvisiontools.models.basemodel import BaseModel
import deepvisiontools.models.timmyolo.utils as ut
from ultralytics.utils.loss import (
    v8DetectionLoss,
    TaskAlignedAssigner,
    BboxLoss,
)
from deepvisiontools.config import Configuration
from deepvisiontools.formats import (
    BatchedFormat,
    BboxFormat,
    InstanceMaskFormat,
    BboxData,
)
from torchvision.transforms.v2 import Pad
from math import ceil
from torch import Tensor
import deepvisiontools.models.timmyolo.errors as er
from dataclasses import dataclass

from typing import Tuple, List, Dict


@dataclass
class LossHyperParams:
    """Used in YoloDetectHead"""

    # Yolo default vals
    box: float = 7.5
    dfl: float = 1.5
    cls: float = 0.5


class YoloLoss(v8DetectionLoss):
    def __init__(self, model, tal_topk=10):
        """Adapting Yolo Loss to TimmYolo."""
        device = Configuration().device  # get model device
        h = model.args  # hyperparameters

        m = model.detect_head  # Detect() module
        self.bce = nn.BCEWithLogitsLoss(reduction="none")
        self.hyp = h
        self.stride = m.stride  # model strides
        self.nc = m.nc  # number of classes
        self.no = m.nc + m.reg_max * 4
        self.reg_max = m.reg_max
        self.device = device

        self.use_dfl = m.reg_max > 1

        self.assigner = TaskAlignedAssigner(
            topk=tal_topk, num_classes=self.nc, alpha=0.5, beta=6.0
        )
        self.bbox_loss = BboxLoss(m.reg_max).to(device)
        self.proj = torch.arange(m.reg_max, dtype=torch.float, device=device)


class TimmYolo(BaseModel):
    """This class combines any timm library encoder compatible with features_only=True with a Yolo detection head.
    This leverage complex encodeur, potentially with attention layers, while remaining flexible on the input image size.
    The idea is to patchify all images that run through the model, perform feature prediction, combine the feature and run the fully convolutional yolo detection head.
    **Note: ** This model does not have a forward method ! use run() or get_predictions instead.

    Args:
        backbone_name (str, optional): timm backbone. Defaults to "swin_small_patch4_window7_224". Has been tested with "vit_large_patch14_dinov2" and "resnet50.a1_in1k" as well
        num_classes (int, optional): Defaults to 1.
        pretrained (bool, optional): Defaults to True.
        overlap (float | int | Tuple[int, int] | None, optional): If different of None use the pixel given value for overlap (careful it must be compatible with the reduction level).
        If none it uses the maximum reduction x 2. Defaults to None.
        internal_batch_size (int, optional): Number of patch to run simultaneously. Defaults to 1.
    """

    def __init__(
        self,
        backbone_name="swin_small_patch4_window7_224",
        num_classes=1,
        pretrained: bool = True,
        overlap: float | int | Tuple[int, int] | None = None,
        internal_batch_size: int = 1,
        loss_factor=100,
    ):

        super().__init__()

        # Load Transformer backbone (from TIMM)
        self.backbone = timm.create_model(
            backbone_name, pretrained=pretrained, features_only=True
        )
        # Get backbone input size
        self.patch_size = self.backbone.pretrained_cfg["input_size"][-2:]

        # Get feature map channels from different stages
        feature_channels = self.backbone.feature_info.channels()
        self.feature_channels = feature_channels
        # reduction factor of features
        self.reds = [it["reduction"] for it in self.backbone.feature_info.info]
        # There is a weird issue with transformers in timm : the reduction info has not the same size as the feature info... Need to readapt
        if len(self.reds) > len(self.feature_channels):
            self.reds = self.reds[0 : len(self.feature_channels)]

        if overlap == None:
            overlap = max(self.reds) * 2

        # YOLO-like detection head (fully convolutional)
        detect_head = Detect(nc=num_classes, ch=feature_channels)
        detect_head.dynamic = True
        self.detect_head = detect_head
        self.detect_head.stride = torch.tensor(self.reds).to(torch.float)
        self.overlap = overlap
        self.patcher = ut.Patcher(self.patch_size, self.overlap)

        self.args = LossHyperParams()

        self.loss = YoloLoss(self)

        self.internal_batch_size = internal_batch_size
        self.loss_factor = loss_factor

    def prepare_target(
        self, targets: BatchedFormat, img_size: Tuple[int, int]
    ) -> Dict[str, Tensor]:
        """Return target from BatchedFormat to ultralytics yolo format.

        Args:
            targets (BatchedFormat)
            img_size (Tuple[int, int])

        Returns:
            Dict[str, Tensor]: target as per ultralytics Yolo format.
        """
        # Convert to BboxFormat if there are InstanceMasks
        if any([isinstance(targ, InstanceMaskFormat) for targ in targets.formats]):
            forms = [
                (
                    BboxFormat.from_instance_mask(targ)
                    if isinstance(targ, InstanceMaskFormat)
                    else targ
                )
                for targ in targets
            ]
            targets = BatchedFormat(forms)
        targets.set_bboxes_format("CXCYWH")
        boxes = torch.cat([targ.data.value for targ in targets])
        boxes = ut.normalize_boxes(boxes, img_size)
        labels = torch.cat([targ.labels for targ in targets])[..., None]
        batch_idx = torch.cat(
            [torch.ones(targ.nb_object) * i for i, targ in enumerate(targets)]
        )[..., None]
        batch_idx = batch_idx.to(Configuration().device)
        return {"batch_idx": batch_idx, "cls": labels, "bboxes": boxes}

    def prepare(
        self, images, targets=None
    ) -> Tuple[Tensor, BatchedFormat | None, torch.Size]:
        """Pad images and target so final patch match exactly image border.

        Args:
            images (``_type_``): image to be prepared
            targets (``_type_``, **optional**): tragets to be prepared. Defaults to None.

        Returns:
            ``Tuple[Tensor, BatchedFormat | None, torch.Size]``:
                - prepared images, prepared targets, original image size
        """
        l, t, r, b = self.patcher.gen_pad_requirements(images.shape[-2:])
        padder = Pad((l, t, r, b))
        prepared_images = padder(images)
        if targets != None:
            prepared_targets = BatchedFormat([ta.pad(l, t, r, b)[0] for ta in targets])
            prepared_targets = self.prepare_target(
                prepared_targets, prepared_images.shape[-2:]
            )
            return prepared_images, prepared_targets, images.shape[-2:]
        else:
            return prepared_images, None, images.shape[-2:]

    def build_results(
        self,
        raw_outputs: List[Tensor],
        prebuild_outputs: Tensor,
        original_img_size: torch.Size,
    ) -> BatchedFormat:
        """Transform model outputs into Batch BboxFormat for results.

        Args:
            raw_outputs (``List[Tensor]``): Model outputs.
            prebuild_outputs (``Tensor``): Extracted boxes from outputs in eval mode.

        Returns:
            ``BatchedFormats``:
                - Batched predictions.
        """

        prebuild_outputs = prebuild_outputs.unbind()
        h, w = self.retrieve_spatial_size(raw_outputs)
        results = []
        # for each prediction
        for prediction in prebuild_outputs:
            # send pred in good pshape
            prediction = prediction.permute(1, 0)
            # get best class and corresponding score
            best_class = torch.argmax(prediction[:, 4:], dim=1)
            confidence, _ = torch.max(prediction[:, 4:], dim=1)
            # gather box cxcywh coordinates
            boxes = BboxData(prediction[:, :4], "CXCYWH", (h, w))
            # build result
            result = BboxFormat(boxes, best_class, scores=confidence)
            # objects selections
            result = ut.confidence_filter(result)
            result = ut.box_nms_filter(result)
            result, _ = result[: Configuration().model_max_detection]
            # stack batch results
            results.append(result)

        if len(results) == 0:
            results = []
        # crop predictions to return original image size preds
        results = BatchedFormat(results)
        cv_size = results.formats[0].canvas_size
        t = int((float(cv_size[0]) - original_img_size[0]) / 2.0)
        l = int((float(cv_size[1]) - original_img_size[1]) / 2.0)
        h, w = original_img_size
        predictions = BatchedFormat([p.crop(t, l, h, w)[0] for p in results])
        return predictions

    def get_predictions(self, images: Tensor):
        self.eval()
        # prepare inputs
        prepared_images, _, original_img_size = self.prepare(images, targets=None)
        # for img in batch do patchification
        patched_imgs: List[Tuple[Tensor, List[Tuple[int, int, int, int]]]] = []
        for prep_img in prepared_images:
            patches, absolute_positions = self.patcher(prep_img, original_img_size)
            patches = torch.stack(patches)
            patched_imgs.append((patches, absolute_positions))
        # infer weight shape from imgs size
        weights_shapes = [
            tuple(ceil(float(s) / r) for s in prepared_images.shape[-2:])
            for r in self.reds
        ]
        prebuild_output, raw_outputs = self.run(patched_imgs, weights_shapes)
        predictions = self.build_results(
            raw_outputs, prebuild_output, original_img_size
        )
        return predictions

    def run_forward(self, images, targets):
        # prepare inputs
        prepared_images, prepared_targets, original_img_size = self.prepare(
            images, targets=targets
        )
        # for img in batch do patchification
        patched_imgs: List[Tuple[Tensor, List[Tuple[int, int, int, int]]]] = []
        for prep_img in prepared_images:
            patches, absolute_positions = self.patcher(prep_img, original_img_size)
            patches = torch.stack(patches)
            patched_imgs.append((patches, absolute_positions))
        # infer weight shape from imgs size
        weights_shapes = [
            tuple(ceil(float(s) / r) for s in prepared_images.shape[-2:])
            for r in self.reds
        ]
        # forward pass
        if self.training:
            raw_outputs = self.run(patched_imgs, weights_shapes)
        else:
            prebuild_output, raw_outputs = self.run(patched_imgs, weights_shapes)

        loss_dict = self.compute_loss(raw_outputs, prepared_targets)
        # return predictions if needed
        if not (self.training):
            predictions = self.build_results(
                raw_outputs, prebuild_output, original_img_size
            )
            return loss_dict, predictions
        else:
            return loss_dict

    def run(
        self,
        patched_imgs: List[Tuple[Tensor, List[Tuple[int, int, int, int]]]],
        weights_shapes: List[Tuple],
    ):
        full_feats = {i: [] for i in range(len(self.reds))}
        for patches, abs_pos in patched_imgs:
            weights: List[Tensor] = [torch.zeros(ws) for ws in weights_shapes]
            feats = self.backbone(patches)
            # permute to get feats : [N_batch, channels, h, w]
            order = [
                (torch.tensor(f.shape) == ch).nonzero().item()
                for f, ch in zip(feats, self.feature_channels)
            ]
            # handles feature channel dimension reordering (N_batch, N_feat, h, w) after backbone reduction
            permutes = []
            for o in order:
                l = [1, 2, 3]
                l.remove(o)
                permutes.append([o] + l)
            feats = [f.permute(0, *o) for f, o in zip(feats, permutes)]
            # merging patched features
            feats = self.merge_features(feats, abs_pos, weights)
            for k in full_feats.keys():
                full_feats[k].append(feats[k])
        # stack patchs and stack imgs to recover batch
        full_feats = [torch.stack(f) for f in full_feats.values()]
        output = self.detect_head(full_feats)
        return output

    def prepare_weights(self, prepared_images: Tensor):
        dims = [
            tuple((int(i / r) for i in prepared_images.shape[-2:])) for r in self.reds
        ]
        feat_weights = [torch.zeros(shape) for shape in dims]
        return feat_weights

    def merge_features(
        self,
        feats: List[Tensor],
        absolute_positions: Tuple[int, int, int, int],
        weights: List[Tensor],
    ):
        # align weights and features according to shape
        sorted(weights, key=lambda x: x.shape[-1])
        sorted(feats, key=lambda x: x.shape[-1])
        # generate 0 filled features from channels size and weight size (which have the final shape of the feature maps)
        merged_feats = [
            torch.zeros((feats[i].shape[1], *weights[i].shape[-2:])).to(feats[0].device)
            for i in range(len(feats))
        ]
        # Loop over feature maps (typically (Ch1, 64, 64), (Ch2, 32, 32), (Ch3, 16, 16), (Ch4, 8, 8)) but depend on encoder
        for i, (mer_feat, feat, weight, r) in enumerate(
            zip(merged_feats, feats, weights, self.reds)
        ):
            # loop over patches
            for f, abs_pos in zip(feat, absolute_positions):
                y1 = int(abs_pos[0] / r)
                x1 = int(abs_pos[1] / r)
                y2 = int((abs_pos[0] + abs_pos[2]) / r)
                x2 = int((abs_pos[1] + abs_pos[3]) / r)
                weight[y1:y2, x1:x2] += 1
                mer_feat[:, y1:y2, x1:x2] += f
            mer_feat /= weight.to(mer_feat.device)

        return merged_feats

    def forward(self, x):
        raise er.NonImplementedForward()

    def retrieve_spatial_size(self, raw_outputs: List[Tensor]) -> Tuple[int]:
        """Retrieve image shape from raw_outputs and stride values.

        Args:
            raw_outputs (``List[Tensor]``): Raw ouptuts from YOLO model.

        Returns:
            ``Tuple[int]``:
                - Size of input image (H, W).
        """
        h = int(raw_outputs[0].shape[-2] * self.detect_head.stride[0])
        w = int(raw_outputs[0].shape[-1] * self.detect_head.stride[0])
        return (h, w)

    def compute_loss(
        self, raw_outputs: Tensor, targets: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Compute loss with predictions & targets.

        Args:
            raw_outputs (``Any``): Raw output of model.
            targets (``DetectionFormat``): Targets in YOLO format.

        Returns:
            ``Dict[str, Tensor]``:
                - Loss dict with total loss (key: "loss") & sublosses.
        """
        # yolo scale loss with batch size -> normalize it here and apply loss factor to keep it in the unit range
        # (for mixed precision optim it's important)
        batch_factor = targets["batch_idx"].unique().shape[0]
        loss, loss_detail = self.loss(raw_outputs, targets)
        loss /= self.loss_factor * batch_factor
        loss_detail /= self.loss_factor * batch_factor
        loss_dict = {
            "loss": loss,
            "loss_box": loss_detail[0],
            "loss_cls": loss_detail[1],
            "loss_dfl": loss_detail[2],
        }
        return loss_dict
