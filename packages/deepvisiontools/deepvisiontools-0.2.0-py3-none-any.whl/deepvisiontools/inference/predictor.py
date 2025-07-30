from deepvisiontools import Configuration
from deepvisiontools.models.basemodel import BaseModel
from typing import Tuple, Union, Callable, Dict
from deepvisiontools.preprocessing.preprocessing import build_preprocessing
from pathlib import Path
import torch
from torch import Tensor
from deepvisiontools.formats import BatchedFormat, BaseFormat
from typing import List, Union
from deepvisiontools.utils import visualization
from deepvisiontools.preprocessing.image import load_image
from deepvisiontools.inference.patchifier import (
    DetectPatchifier,
    SemanticPatchifier,
    BasePatchifier,
)
from torchvision.transforms.v2 import Pad, CenterCrop
from tqdm import tqdm
from deepvisiontools.formats import SemanticMaskData, SemanticMaskFormat


def build_patchifier(*args, **kwargs):
    if Configuration().data_type == "semantic_mask":
        return SemanticPatchifier(*args, **kwargs)
    else:
        return DetectPatchifier(*args, **kwargs)


class Predictor:
    """Predictor class for deepvisiontools. Load a model and apply on image, get prediction. Can handle patchification for large image prediction.

    Args:
        model (``Union[BaseModel, str, Path]``): model path / instance of BaseModel to be used.
        preprocessing (``Callable``, **optional**): used preprocesser. Defaults to build_preprocessing().
        patch_size (``Union[Tuple[int, int], None]``, **optional**): size of the patchs to be used for large image inference. If None will run the full image. Defaults to None.
        overlap (``float``, **optional**): Overlap between patches used in case of patchification. Defaults to 0.4.
        border_padding (``int``, **optional**): default image padding when using patchification. Defaults to 100.
        batch_size (``int``, **optional**): batch size for patchification. Defaults to 1.
        border_penalty (``float``, **optional**): apply a penalty on patch border predictions : makes nms more efficient. Higher is more stringent. Max to 1 and Min to 0. Defaults to 0.5.
        nms_iou_threshold (``float``, **optional**): nms threshold to be used when upatchifying. Defaults to 0.45.
        final_score_threshold (``float``, **optional**): Apply a score thresholding after penalty and after nms. Defaults to 0.4.
        categories (``Dict[int, str]``, **optional**): To rename your categories in the visualization.
        patchifier (``Union[BasePatchifier, None], **optional**): If None use default SemanticPatchifier or DetectPatchifier according to Configuration().data_type. Default to None.
        verbose (``bool``, **optional**) : if set to True will display progress state in patchs predictions. Default to True.

    Example:
    ----------

    .. highlight:: python
    .. code-block:: python

        >>> from deepvisiontools import Predictor
        >>> img = \"path/to/img\"
        >>> predictor = Predictor(model=\path\to\model.pth)
        >>> results = predictor.predict(img)

    Attributes
    ----------

    Attributes:
        model (``BaseModel``)
        preprocessing (``Callable``)
        patch_size (``Union[Tuple[int, int], None]``)
        padder (``Transform``)
        batch_size (``int``)
        cropper (``Transform``)
        patchifier (``BasePatchifier``)
        categories (``Dict[int, str]``)
        verbose (``bool``)


    **Methods**
    """

    def __init__(
        self,
        model: Union[BaseModel, str, Path],
        preprocessing: Callable = build_preprocessing(),
        patch_size: Union[Tuple[int, int], None] = None,
        overlap: float = 0.4,
        border_padding: int = 100,
        batch_size: int = 1,
        categories: Dict[int, str] = None,
        patchifier: Union[BasePatchifier, None] = None,
        verbose: bool = True,
    ):
        assert any(
            [
                isinstance(model, BaseModel),
                isinstance(model, Path),
                isinstance(model, str),
            ]
        ), "model must be instance of BaseModel or path to model"
        if not isinstance(model, BaseModel):
            model = Path(model) if isinstance(model, str) else model
            assert model.exists(), f"model path does not exists, got {model.as_posix()}"
            model = torch.load(model, map_location=Configuration().device)
        self.model: BaseModel = model.to(Configuration().device).eval()
        self.patch_size = patch_size
        self.batch_size = batch_size
        self.preprocessing = preprocessing
        self.padder = Pad(border_padding)
        self.cropper = None  # is updated in self.predict

        if patchifier == None:
            self.patchifier = build_patchifier(self.patch_size, overlap)
        else:
            self.patchifier = patchifier
        self.categories = categories
        self.verbose = verbose

    def forward_pass(self, batch_patchs: Tensor) -> BatchedFormat:
        """Run predictions on image / batch of patches"""
        with torch.no_grad():
            loader = PredictorDataLoader(batch_patchs, self.batch_size)
            # wrap in tqdm if more than one batch
            if self.verbose:
                loader = (
                    tqdm(
                        loader, desc="Predict on batch of patches : ", total=len(loader)
                    )
                    if len(loader) > 1
                    else loader
                )
            predictions = BatchedFormat([])

            for patch in loader:
                with torch.autocast(
                    device_type=Configuration().device,
                    dtype=torch.float16,
                    enabled=Configuration().optimize,
                ):
                    predictions += self.model.get_predictions(patch)
        return predictions

    def predict(
        self,
        image: Union[str, Path, Tensor],
        visu_path: Union[str, Path] = "",
    ) -> BaseFormat:
        """Main function of ```Predictor``` : call everything needed for prediction.

        Args:
            image (``Union[str, Path, Tensor]``): _description_
            visu_path (``Union[str, Path]``, **optional**): path to visualization to be saved. Defaults to "".

        Returns:
            ``BaseFormat``:
                - prediction as deepvisiontools format.
        """
        # Load image if needed
        if isinstance(image, str):
            image = Path(image)
            image: Tensor = load_image(image)
        if isinstance(image, Path):
            image = load_image(image)
        # pad image
        self.cropper = CenterCrop(image.shape[-2:])
        h_original, w_original = image.shape[-2:]
        image = image.to(Configuration().device)
        # preprocess
        if self.preprocessing != None:
            preprocessed_image = self.preprocessing(image[None, :])[0]
        else:
            preprocessed_image = image
        # handles patch if needed
        if self.patch_size != None and self.patch_size != (
            image.shape[-2],
            image.shape[-1],
        ):
            _h_pad, _w_pad = 0, 0
            if image.shape[-2] < self.patch_size[0]:
                _h_pad = self.patch_size[0] - image.shape[-2]
                _t_pad = int(_h_pad // 2)
                _t_pad = _t_pad if _t_pad > 0 else 0
                _b_pad = _h_pad - _t_pad
                _b_pad = _b_pad if _b_pad > 0 else 0
            if image.shape[-2] < self.patch_size[0]:
                _w_pad = self.patch_size[1] - image.shape[-1]
                _l_pad = int(_w_pad // 2)
                _l_pad = _l_pad if _l_pad > 0 else 0
                _r_pad = _w_pad - _l_pad
                _r_pad = _r_pad if _r_pad > 0 else 0
            if _h_pad > 0 or _w_pad > 0:
                preprocessed_image = Pad((_l_pad, _t_pad, _r_pad, _b_pad))(
                    preprocessed_image
                )

            batch_patch, pad_origins, padded_image, pad_coord = (
                self.patchifier.patchify(preprocessed_image)
            )
            h_pad, w_pad = padded_image.shape[-2:]
            preds = self.forward_pass(batch_patch)
            # filter empty patches and associated origins
            preds, pad_origins = self.filter_empty_patches(preds, pad_origins)
            # unpatchification
            preds = self.patchifier.unpatchify(
                preds, pad_origins, (h_pad, w_pad), pad_coord, (h_original, w_original)
            )
        else:
            preds = self.forward_pass(
                preprocessed_image[None, :]
            )  # forward_pass need batch image -> add dummy dim
            preds = preds.formats[0]
        # recover pre-border-padding shape
        preds, _, _ = preds.apply_augmentation(image, self.cropper)
        # Create visualization if needed
        if visu_path:
            visu_path = visu_path if isinstance(visu_path, Path) else Path(visu_path)
            visualization(image, preds, categories=self.categories, save_path=visu_path)
        return preds

    def filter_empty_patches(
        self, preds_batch_patch: BatchedFormat, pad_origins: List[Tuple[int, int]]
    ):
        """remove empty patches for unpatchification"""
        filter_empty = [
            False if pred.nb_object == 0 else True for pred in preds_batch_patch
        ]
        pad_origins = [el for i, el in enumerate(pad_origins) if filter_empty[i]]
        preds_batch_patch = preds_batch_patch[torch.tensor(filter_empty)]
        return preds_batch_patch, pad_origins


class PredictorDataLoader:
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
