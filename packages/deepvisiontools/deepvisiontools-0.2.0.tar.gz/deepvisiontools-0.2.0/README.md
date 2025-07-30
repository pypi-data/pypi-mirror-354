<!--
<p align="center">
  <img src="https://github.com///raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  deepvisiontools
</h1>


Torch overlay for trainning and inference processes for object detection & instance segmentation tasks. 

## 💪 Context

deepvisiontools is developped by INRAE (french National Research Institute for Agriculture, Food and the Environment) and in [PHENOME-EMPHASIS project](https://www.phenome-emphasis.fr/).

## Citations

deepvisiontools provides model wrappers that allow you to use differents models with all machinery available. It is the responsability of the user to cite properly the actual model developpers.
In particular, if using one of these models : Yolo, SMP please cite the actual models developpers (which are not deepvisiontools). For instance for Yolo, please cite ultralytics (https://www.ultralytics.com/) or for SMP cite https://github.com/qubvel-org/segmentation_models.pytorch  
Similar stands for other models.
TimmYolo model is a new model that combines timm encoders with a Yolo detection head. The strategy is based on patchification for the backbone (to avoid loosing resolution in resizing) then merge the features before running a Yolo detection heads. If you use this wrapper please cite both timm library, ultralytics library as well as deepvisiontools as model developper.

## Documentation

All documentation about deepvisiontools, including tutorials, can be found at : https://deepvisiontools.readthedocs.io/en/latest/

## Installation
We have tested deepvisiontools for python versions between 3.11.9 and 3.12.11, we recommend to use python 3.12.11 to minimize the risk of bugs.

```shell
pip install deepvisiontools
```
If you wish to use TimmYolo model, you may encounter an error saying that feature_only is not available for a given encoder name. Please upgrade your timm version (1.0.15 should have most of them). You may need to reinstall deepvisiontools as you could create conflicts with segmentation-models-pytorch.
## License

GNU Affero General Public License v3 or later (AGPLv3+) (AGPL-3.0).


