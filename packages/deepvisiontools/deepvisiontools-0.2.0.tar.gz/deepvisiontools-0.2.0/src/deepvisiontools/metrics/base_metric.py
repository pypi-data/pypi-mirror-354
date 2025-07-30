from typing import Any, Callable, Dict, List, Tuple, Union
from deepvisiontools.formats import (
    BatchedFormat,
    BaseFormat,
    InstanceMaskFormat,
    SemanticMaskFormat,
)
import torch
from torch import Tensor
from torchmetrics import Metric
from deepvisiontools.metrics.matcher import Matcher
from deepvisiontools import Configuration
from torchmetrics.classification import StatScores


class DetectMetric(Metric):
    """Base class for custom detection metric with torchmetrics engine

    Args:
        func (Callable): function to apply to tp, fp, tn, fn
        name (str, optional): metric's name (useful for tensorboard monitoring). Defaults to "DetectionMetric".
    """

    is_differentiable = None
    higher_is_better = True
    full_state_update: bool = False

    def __init__(
        self,
        func: Callable,
        name: str = "DetectionMetric",
        **kwargs,
    ):
        assert (
            Configuration().data_type != "semantic_mask"
        ), "Can't use detection metrics with Configuration().data_type = semantic_mask. Must be instance_mask or bbox"
        super().__init__(**kwargs)
        self.func = func
        self.name = name
        self.add_state("stats", default=[], dist_reduce_fx="cat")
        self.nc = 1  # always one class

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Update metric's internal state with prediction target comparison (tp, fp, tn, fn)

        Args:
            prediction (Union[BaseFormat, BatchedFormat])
            target (Union[BaseFormat, BatchedFormat])
        """

        # if no objects in prediction or target: stats are neutral (0)
        # else compute match box and stats

        # Cast pred and target to batched format if not already batched format
        prediction: BatchedFormat = (
            prediction
            if isinstance(prediction, BatchedFormat)
            else BatchedFormat([prediction])
        )
        target: BatchedFormat = (
            target if isinstance(target, BatchedFormat) else BatchedFormat([target])
        )
        # update metric
        matcher = Matcher()
        for pred, targ in zip(prediction, target):
            if pred.nb_object != 0 and targ.nb_object != 0:
                tp, fp, fn, _ = matcher.match_pred_target(pred, targ)
            elif pred.nb_object != 0 and targ.nb_object == 0:
                tp, fp, fn, _ = 0, pred.nb_object, 0, None
            # elif prediction.size == 0 and target.size != 0:
            elif pred.nb_object == 0 and targ.nb_object != 0:
                tp, fp, fn, _ = 0, 0, targ.nb_object, None
            else:
                tp, fp, fn, _ = torch.nan, torch.nan, torch.nan, None

            # NaN because of no tn in detection
            self.stats.append(
                torch.tensor([[[tp, fp, torch.nan, fn, torch.nan]]])
            )  # fix tn and support to nan

    def global_micro_compute(self) -> Tensor:
        """Compute metric with global/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.nansum(dim=0)  # (NC, 5)
        # sum stats accross classes
        micro_stack = torch.nansum(samples_stack, dim=0)  # (5,)
        # compute metric
        tp, fp, tn, fn, _ = micro_stack.unbind(0)
        return self.func(tp, fp, tn, fn)

    def samplewise_micro(self) -> Tensor:
        """Compute metric with samplewise/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5))
        # sum stat accross classes
        samples_stack = samples_stack.nansum(dim=1)  # (NC, 5)
        # compute metric/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(dim=1)
        samples_metrics = self.func(tp, fp, tn, fn)
        # mean accross samples
        return torch.nanmean(samples_metrics)

    def compute_last_sample(self):
        """Return metrics values of the last sample in self.stats.
            Used in combination with self.update

        Returns:
             Dict[str, Float]: dictionnary with metric value for all classes combined and for each class
        """

        if not self.stats:
            return {"all_cls": torch.tensor(torch.nan)}

        metric_sample_dict = {}

        matrix_stats_img = self.stats[-1].squeeze(
            0
        )  # matrix with stats (tp, fp, tn, fn) of one sample (one row for each class)
        nb_class = matrix_stats_img.size(dim=0)
        tp, fp, tn, fn, _ = matrix_stats_img.nansum(dim=0).unbind(
            dim=0
        )  # sum over all classes
        all_class_metric_value = round(
            self.func(tp, fp, tn, fn).item(), 3
        )  # metric compute for all classes
        metric_sample_dict["all_cls"] = all_class_metric_value

        if nb_class > 1:
            for index_class in range(nb_class):  # metric compute for each class
                matrix_stats_img_class = matrix_stats_img[index_class, :]
                tp, fp, tn, fn, _ = matrix_stats_img_class.unbind(
                    dim=0
                )  # stats (tp, fp, tn, fn) of the given class
                class_metric_value = round(
                    self.func(tp, fp, tn, fn).item(), 3
                )  # metric compute for the given class
                metric_sample_dict["cls_{0}".format(index_class)] = class_metric_value

        return metric_sample_dict

    def compute(self) -> Dict[str, Tensor]:
        """Return metric computed with internal state.

        Returns:
             Dict[str, Tensor]: dictionnary with aggregation_method: value
        """
        if not self.stats:
            return {self.name: torch.tensor(torch.nan)}

        # global micro
        global_value = self.global_micro_compute()
        # samplewise micro
        samplewise_value = self.samplewise_micro()

        metric_dict = {"global": global_value, "samplewise": samplewise_value}

        return metric_dict


class ClassWiseDetectMetric(Metric):
    """Base class that agregates n_classes DetectMetric(s) to obtain class dependant performances.
    Note that samplewise scores are not performed here.

    Args:
        func (Callable): function to apply to tp, fp, tn, fn
        name (str, optional): metric's name (useful for tensorboard monitoring). Defaults to "ClassWiseDetectionMetric".

    Attributes
    ----------

    Attributes:
        - classmetrics (``List[DetectMetric]``): list of detectmetrics specialized in each classes.
    """

    def __init__(
        self,
        func: Callable,
        name: str = "ClassWiseDetectionMetric",
        **kwargs,
    ):
        assert (
            Configuration().data_type != "semantic_mask"
        ), "Can't use detection metrics with Configuration().data_type = semantic_mask. Must be instance_mask or bbox"
        num_classes = Configuration().num_classes
        self.nc = num_classes
        assert (
            num_classes >= 2
        ), f"{num_classes} is an invalid number of classes for ClassWiseMetric (must be >= 2). If you have one class please use DetectMetric instead of ClasswiseMetric"

        super().__init__(**kwargs)
        self.name = name

        # create instances of DetectMetrics : 1 for global and 1 for each class
        self.classmetrics = [DetectMetric(func, name=f"{name}/global").to(self.device)]
        self.classmetrics += [
            DetectMetric(func, name=f"{name}/cls_{i}").to(self.device)
            for i in range(num_classes)
        ]
        self.add_state("stats", default=[], dist_reduce_fx="cat")
        self.func = func

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Update all DetectMetrics in self.classmetrics according to prediction / target.

        Args:
            prediction (Union[BaseFormat, BatchedFormat])
            target (Union[BaseFormat, BatchedFormat])
        """
        prediction = (
            prediction
            if isinstance(prediction, BatchedFormat)
            else BatchedFormat([prediction])
        )
        target = (
            target if isinstance(target, BatchedFormat) else BatchedFormat([target])
        )
        list_met_class = []
        for i, met in enumerate(self.classmetrics):
            met_samples_result = []
            if i == 0:
                met.update(prediction, target)
            else:
                filtered_pred = self._filter_classes(
                    prediction, i - 1
                )  # -1 because classes start at 0
                filtered_targ = self._filter_classes(target, i - 1)
                met.update(filtered_pred, filtered_targ)

            # retrieve and save in a list the stats for each sample in the batch for the given class
            batch_size = prediction.size
            for num_elem in range(batch_size, 0, -1):
                met_samples_result.append(met.stats[-num_elem])

            list_met_class.append(
                met_samples_result
            )  # save the list in the list containing the list of each class

        # save the batch sample stats for each class in a matrix (N, NC, 5) and append in metric 'stats' attribute
        for num_sample in range(batch_size):
            sample_stats = []
            for num_class in range(1, len(list_met_class)):
                sample_stats.append(list_met_class[num_class][num_sample])

            class_stack = torch.cat(sample_stats).view(
                1, Configuration().num_classes, 5
            )  # (N, NC, 5)
            self.stats.append(class_stack)

        # for sample_list_met_class in list_met_class:
        #     sample_list_met_class = sample_list_met_class[1:]
        #     class_stack = torch.cat(sample_list_met_class).view(1, Configuration().num_classes, 5)  # (N, NC, 5)
        #     self.stats.append(class_stack)

    def _filter_classes(self, batchedformat: BatchedFormat, cls: int):
        new_formats = []
        for form in batchedformat:
            new_form, _ = form[form.labels == cls]
            new_formats.append(new_form)
        return BatchedFormat(new_formats)

    def global_micro_compute(self) -> Tensor:
        """Compute metric with global/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.nansum(dim=0)  # (NC, 5)
        # sum stats accross classes
        micro_stack = torch.nansum(samples_stack, dim=0)  # (5,)
        # compute metric
        tp, fp, tn, fn, _ = micro_stack.unbind(0)
        return self.func(tp, fp, tn, fn)

    def global_macro_compute(self) -> Tuple[Tensor, Tensor]:
        """Compute metric with global/macro averraging.
        Return also metric/class tensor."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.nansum(dim=0)  # (NC, 5)
        # compute metric/class
        tp, fp, tn, fn, _ = samples_stack.unbind(1)
        class_metrics = self.func(tp, fp, tn, fn)  # (NC,)
        return torch.nanmean(class_metrics), class_metrics

    def samplewise_micro(self) -> Tensor:
        """Compute metric with samplewise/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5))
        # sum stat accross classes
        samples_stack = samples_stack.nansum(dim=1)  # (N, 5)
        # compute metric/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(dim=1)
        samples_metrics = self.func(tp, fp, tn, fn)
        # mean accross samples
        return torch.nanmean(samples_metrics)

    def samplewise_macro(self) -> Tensor:
        """Compute metric with samplewise/macro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # compute metric/class/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(2)
        class_metrics = self.func(tp, fp, tn, fn)  # (N,NC)
        # mean accross classes
        macro = torch.nanmean(class_metrics, dim=1)  # (N,)
        # mean accross samples
        macro_samplewise = torch.nanmean(macro, dim=0)

        return macro_samplewise

    def compute_last_sample(self):
        """Return metrics values of the last sample in self.stats.
            Used in combination with self.update

        Returns:
             Dict[str, Float]: dictionnary with metric value for all classes combined and for each class
        """

        if not self.stats:
            return {"all_cls": torch.tensor(torch.nan)}

        metric_sample_dict = {}

        matrix_stats_img = self.stats[-1].squeeze(
            0
        )  # matrix with stats (tp, fp, tn, fn) of one sample (one row for each class)
        nb_class = matrix_stats_img.size(dim=0)
        tp, fp, tn, fn, _ = matrix_stats_img.nansum(dim=0).unbind(
            dim=0
        )  # sum over all classes
        all_class_metric_value = round(
            self.func(tp, fp, tn, fn).item(), 3
        )  # metric compute for all classes
        metric_sample_dict["all_cls"] = all_class_metric_value

        if nb_class > 1:
            for index_class in range(nb_class):  # metric compute for each class
                matrix_stats_img_class = matrix_stats_img[index_class, :]
                tp, fp, tn, fn, _ = matrix_stats_img_class.unbind(
                    dim=0
                )  # stats (tp, fp, tn, fn) of the given class
                class_metric_value = round(
                    self.func(tp, fp, tn, fn).item(), 3
                )  # metric compute for the given class
                metric_sample_dict["cls_{0}".format(index_class)] = class_metric_value

        return metric_sample_dict

    def compute(self):
        """Return metrics values.

        Returns:
             Dict[str, Tensor]: dictionnary with all "global" DetectMetric in self.classmetrics
        """
        # classwisedict = {met.name: met.compute()["global"] for met in self.classmetrics}
        # return classwisedict

        if not self.stats:
            return {self.name: torch.tensor(torch.nan)}

        metric_dict = {}
        # global micro
        global_micro = self.global_micro_compute()
        metric_dict.update({"_global_micro": global_micro})
        # global macro
        global_macro, class_metrics = self.global_macro_compute()
        classes_dict = {
            f"/cls_{i}": class_metrics[i] for i in range(class_metrics.nelement())
        }
        metric_dict.update({"_global_macro": global_macro})
        metric_dict.update(classes_dict)
        # samplewise micro
        samplewise_micro = self.samplewise_micro()
        metric_dict.update({"_samplewise_micro": samplewise_micro})
        # samplewise macro
        samplewise_macro = self.samplewise_macro()
        metric_dict.update({"_samplewise_macro": samplewise_macro})

        return metric_dict

    # override
    def reset(self):
        """Reset all metrics in self.classmetrics. Override from torchmetrics Metric"""
        [met.reset() for met in self.classmetrics]

    # override
    def to(self, device: Any):
        """Move all metrics in self.classmetrics to device. Override from torchmetrics Metric

        Args:
            device (Any)
        """
        self.classmetrics = [metric.to(device) for metric in self.classmetrics]
        return self


class ClassifMetric(Metric):
    """Child class of torchmetrics metrics for classification.
    Allow to take Format as inputs and return dict of metric."""

    def __init__(
        self,
        func: Callable,  # metric functionnal
        name: str = "ClassifMetric",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        num_classes = Configuration().num_classes
        self.func = func
        self.task = "binary" if num_classes == 1 else "multiclass"
        self.nc = num_classes
        # use tm engine to get statistics (tp,tn,fp,fn,sup)
        self.stat_score = StatScores(
            task=self.task,
            multidim_average="samplewise",
            average="none",
            num_classes=num_classes,
        )
        self.add_state("stats", default=[], dist_reduce_fx="cat")
        self.name = name

    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        assert (
            Configuration().data_type != "semantic_mask"
        ), "Can't use ClassifMetric with Configuration().data_type = semantic_mask. Must be instance_mask or bbox"
        """Update internal states."""
        # if no predictions or target, no classification evaluation
        prediction = (
            BatchedFormat([prediction])
            if not isinstance(prediction, BatchedFormat)
            else prediction
        )
        target = (
            BatchedFormat([target]) if not isinstance(target, BatchedFormat) else target
        )
        for pred, targ in zip(prediction, target):
            if pred.nb_object == 0 or targ.nb_object == 0:
                return
            target_labels = targ.labels
            # match objects
            matcher = Matcher()
            _, _, _, (pred_idxs, target_idxs) = matcher.match_pred_target(pred, targ)
            pred_idxs = pred_idxs.to(pred.device)
            target_idxs = target_idxs.to(targ.device)
            pred, _ = pred[pred_idxs]
            targ, _ = targ[target_idxs]
            # if no box match, add all targets in fn
            if pred.nb_object == 0:
                class_stats = torch.zeros((self.nc, 5)).to(pred.device)
                values = torch.tensor(
                    [torch.sum(target_labels == i) for i in range(self.nc)]
                )
                class_stats[:, 4] = values
                self.stats.append(class_stats[None, ...])
                return
            # get labels
            pred_labels = pred.labels
            target_labels = targ.labels
            # if binary pass label 0 to 1
            if self.task == "binary":
                pred_labels += 1
                target_labels += 1
            # compute stats
            stats = self.stat_score(
                pred_labels[None, ...], target_labels[None, ...]
            ).view(1, self.nc, 5)
            self.stats.append(stats)

    def global_micro_compute(self) -> Tensor:
        """Compute metric with global/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.nansum(dim=0)  # (NC, 5)
        # sum stats accross classes
        micro_stack = torch.nansum(samples_stack, dim=0)  # (5,)
        # compute metric
        tp, fp, tn, fn, _ = micro_stack.unbind(0)
        return self.func(tp, fp, tn, fn)

    def global_macro_compute(self) -> Tuple[Tensor, Tensor]:
        """Compute metric with global/macro averraging.
        Return also metric/class tensor."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # sum stats accross samples
        samples_stack = samples_stack.nansum(dim=0)  # (NC, 5)
        # compute metric/class
        tp, fp, tn, fn, _ = samples_stack.unbind(1)
        class_metrics = self.func(tp, fp, tn, fn)  # (NC,)
        return torch.nanmean(class_metrics), class_metrics

    def samplewise_micro(self) -> Tensor:
        """Compute metric with samplewise/micro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5))
        # sum stat accross classes
        samples_stack = samples_stack.nansum(dim=1)  # (NC, 5)
        # compute metric/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(dim=1)
        samples_metrics = self.func(tp, fp, tn, fn)
        # mean accross samples
        return torch.nanmean(samples_metrics)

    def samplewise_macro(self) -> Tensor:
        """Compute metric with samplewise/macro averagging."""
        n_samples = len(self.stats)
        samples_stack = torch.cat(self.stats).view(n_samples, self.nc, 5)  # (N, NC, 5)
        # compute metric/class/sample
        tp, fp, tn, fn, _ = samples_stack.unbind(2)
        class_metrics = self.func(tp, fp, tn, fn)  # (N,NC)
        # mean accross classes
        macro = torch.nanmean(class_metrics, dim=1)  # (N,)
        # mean accross samples
        macro_samplewise = torch.nanmean(macro, dim=0)

        return macro_samplewise

    def compute_last_sample(self):
        """Return metrics values of the last sample in self.stats.
            Used in combination with self.update

        Returns:
             Dict[str, Float]: dictionnary with metric value for all classes combined and for each class
        """

        if not self.stats:
            return {"all_cls": torch.tensor(torch.nan)}

        metric_sample_dict = {}

        matrix_stats_img = self.stats[-1].squeeze(
            0
        )  # matrix with stats (tp, fp, tn, fn) of one sample (one row for each class)
        nb_class = matrix_stats_img.size(dim=0)
        tp, fp, tn, fn, _ = matrix_stats_img.nansum(dim=0).unbind(
            dim=0
        )  # sum over all classes
        all_class_metric_value = round(
            self.func(tp, fp, tn, fn).item(), 3
        )  # metric compute for all classes
        metric_sample_dict["all_cls"] = all_class_metric_value

        if nb_class > 1:
            for index_class in range(nb_class):  # metric compute for each class
                matrix_stats_img_class = matrix_stats_img[index_class, :]
                tp, fp, tn, fn, _ = matrix_stats_img_class.unbind(
                    dim=0
                )  # stats (tp, fp, tn, fn) of the given class
                class_metric_value = round(
                    self.func(tp, fp, tn, fn).item(), 3
                )  # metric compute for the given class
                metric_sample_dict["cls_{0}".format(index_class)] = class_metric_value

        return metric_sample_dict

    def compute(self):
        """Comput metric with all averag strategy and return a dict with all values."""
        if not self.stats:
            return {self.name: torch.tensor(torch.nan)}
        # if binary no need for macro aggregation
        metric_dict = {}
        if self.task == "multiclass":
            # global micro
            global_micro = self.global_micro_compute()
            metric_dict.update({"_global_micro": global_micro})
            # global macro
            global_macro, class_metrics = self.global_macro_compute()
            if Configuration().data_type == "semantic_mask":
                classes_dict = {
                    f"/cls_{i+1}": class_metrics[i]
                    for i in range(class_metrics.nelement())
                }
            else:
                classes_dict = {
                    f"/cls_{i}": class_metrics[i]
                    for i in range(class_metrics.nelement())
                }
            metric_dict.update({"_global_macro": global_macro})
            metric_dict.update(classes_dict)
            # samplewise micro
            samplewise_micro = self.samplewise_micro()
            metric_dict.update({"_samplewise_micro": samplewise_micro})
            # samplewise macro
            samplewise_macro = self.samplewise_macro()
            metric_dict.update({"_samplewise_macro": samplewise_macro})
        else:
            # global micro
            global_micro = self.global_micro_compute()
            metric_dict.update({"_global": global_micro})
            # samplewise micro
            samplewise_micro = self.samplewise_micro()
            metric_dict.update({"_samplewise": samplewise_micro})
            return metric_dict

        return metric_dict


class SemanticSegmentationMetric(ClassifMetric):
    """Child class of ClassifMetric. Move from instance to semantic segmentation paradigm to provide stats based on classes masks (instead of objects)."""

    def __init__(
        self,
        func: Callable,  # metric functionnal
        name: str = "SegmentationMetric",
        **kwargs: Any,
    ):
        assert Configuration().data_type in [
            "instance_mask",
            "semantic_mask",
        ], f"Configuration().data_type must be instance_mask or semantic_mask to use SemanticSegmentationMetrics. Got {Configuration().data_type}"
        # init from ClassifMetric and
        # redefine stat score num_classes for multiclass detection to include background as a class (+1 class)
        # Note that background is later removed in update (background is meaningless regarding instance segmentation) but important for stats calculations
        num_classes = Configuration().num_classes
        super().__init__(func, name, **kwargs)
        # Include background if data_type is instance_mask and num_classes != 1
        if num_classes > 1 and Configuration().data_type != "semantic_mask":
            self.stat_score.num_classes = num_classes + 1
        # redefine internal number of classes to remove background from semantic mask (background removal is important to avoid super high scores)
        if (
            Configuration().data_type == "semantic_mask"
            and Configuration().num_classes > 1
        ):
            self.nc -= 1

    # override
    def update(
        self,
        prediction: Union[BaseFormat, BatchedFormat],
        target: Union[BaseFormat, BatchedFormat],
    ):
        """Convert target & prediction to semantic mask to compute stats in semantic segmentation paradigm. Update internal state."""
        prediction = (
            BatchedFormat([prediction])
            if not isinstance(prediction, BatchedFormat)
            else prediction
        )
        target = (
            BatchedFormat([target]) if not isinstance(target, BatchedFormat) else target
        )
        assert type(prediction.formats[0]) in [
            InstanceMaskFormat,
            SemanticMaskFormat,
        ] and type(target.formats[0]) in [
            InstanceMaskFormat,
            SemanticMaskFormat,
        ], "formats of BatchedFormat must be InstanceMaskFormat or SemanticMaskFormat to use SemanticSegmentationMetric"
        # Convert instance mask to semantic mask format
        if isinstance(target.formats[0], InstanceMaskFormat):
            target = BatchedFormat(
                [SemanticMaskFormat.from_instance_mask(t) for t in target]
            )
        if isinstance(prediction.formats[0], InstanceMaskFormat):
            prediction = BatchedFormat(
                [SemanticMaskFormat.from_instance_mask(p) for p in prediction]
            )
        for pred, targ in zip(prediction, target):
            # handling empty target
            pred = pred.data.value
            targ = targ.data.value
            # flatten and add dummy dim for stat score
            flatpred = pred.flatten()[None, :]
            flattarget = targ.flatten()[None, :]
            if self.task == "binary":
                self.stats.append(self.stat_score(flatpred, flattarget))
            else:
                # for multiclass will remove the background scores to avoid crazy high scores
                self.stats.append(self.stat_score(flatpred, flattarget)[:, 1:, :])
