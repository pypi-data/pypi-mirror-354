from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RawTensorsOutput(_message.Message):
    __slots__ = ("tensors",)
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    tensors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, tensors: _Optional[_Iterable[str]] = ...) -> None: ...

class StandardOutput(_message.Message):
    __slots__ = ("boxes_tensor", "scores_tensor")
    BOXES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    SCORES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    boxes_tensor: str
    scores_tensor: str
    def __init__(self, boxes_tensor: _Optional[str] = ..., scores_tensor: _Optional[str] = ...) -> None: ...

class InstanceSegmentationOutput(_message.Message):
    __slots__ = ("boxes_tensor", "scores_tensor", "classes_tensor", "masks_tensor")
    BOXES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    SCORES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    CLASSES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    MASKS_TENSOR_FIELD_NUMBER: _ClassVar[int]
    boxes_tensor: str
    scores_tensor: str
    classes_tensor: str
    masks_tensor: str
    def __init__(self, boxes_tensor: _Optional[str] = ..., scores_tensor: _Optional[str] = ..., classes_tensor: _Optional[str] = ..., masks_tensor: _Optional[str] = ...) -> None: ...

class AnchoredOutput(_message.Message):
    __slots__ = ("anchors_tensor", "offsets_tensor", "scores_tensor")
    ANCHORS_TENSOR_FIELD_NUMBER: _ClassVar[int]
    OFFSETS_TENSOR_FIELD_NUMBER: _ClassVar[int]
    SCORES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    anchors_tensor: str
    offsets_tensor: str
    scores_tensor: str
    def __init__(self, anchors_tensor: _Optional[str] = ..., offsets_tensor: _Optional[str] = ..., scores_tensor: _Optional[str] = ...) -> None: ...

class DirectOutput(_message.Message):
    __slots__ = ("boxes_tensor", "scores_tensor", "classes_tensor")
    BOXES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    SCORES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    CLASSES_TENSOR_FIELD_NUMBER: _ClassVar[int]
    boxes_tensor: str
    scores_tensor: str
    classes_tensor: str
    def __init__(self, boxes_tensor: _Optional[str] = ..., scores_tensor: _Optional[str] = ..., classes_tensor: _Optional[str] = ...) -> None: ...

class YoloOutput(_message.Message):
    __slots__ = ("output_tensor", "anchors")
    OUTPUT_TENSOR_FIELD_NUMBER: _ClassVar[int]
    ANCHORS_FIELD_NUMBER: _ClassVar[int]
    output_tensor: str
    anchors: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, output_tensor: _Optional[str] = ..., anchors: _Optional[_Iterable[float]] = ...) -> None: ...

class YoloV3Output(_message.Message):
    __slots__ = ("output_tensors", "anchors")
    OUTPUT_TENSORS_FIELD_NUMBER: _ClassVar[int]
    ANCHORS_FIELD_NUMBER: _ClassVar[int]
    output_tensors: _containers.RepeatedScalarFieldContainer[str]
    anchors: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, output_tensors: _Optional[_Iterable[str]] = ..., anchors: _Optional[_Iterable[float]] = ...) -> None: ...

class PostProcessing(_message.Message):
    __slots__ = ("anchored_output", "direct_output", "yolo_output", "yolov3_output", "tensors_output", "standard_output", "instance_segmentation_output", "expand_batch_dim")
    ANCHORED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    DIRECT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    YOLO_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    YOLOV3_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TENSORS_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    STANDARD_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_SEGMENTATION_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EXPAND_BATCH_DIM_FIELD_NUMBER: _ClassVar[int]
    anchored_output: AnchoredOutput
    direct_output: DirectOutput
    yolo_output: YoloOutput
    yolov3_output: YoloV3Output
    tensors_output: RawTensorsOutput
    standard_output: StandardOutput
    instance_segmentation_output: InstanceSegmentationOutput
    expand_batch_dim: bool
    def __init__(self, anchored_output: _Optional[_Union[AnchoredOutput, _Mapping]] = ..., direct_output: _Optional[_Union[DirectOutput, _Mapping]] = ..., yolo_output: _Optional[_Union[YoloOutput, _Mapping]] = ..., yolov3_output: _Optional[_Union[YoloV3Output, _Mapping]] = ..., tensors_output: _Optional[_Union[RawTensorsOutput, _Mapping]] = ..., standard_output: _Optional[_Union[StandardOutput, _Mapping]] = ..., instance_segmentation_output: _Optional[_Union[InstanceSegmentationOutput, _Mapping]] = ..., expand_batch_dim: bool = ...) -> None: ...

class PostProcessings(_message.Message):
    __slots__ = ("postprocessings",)
    POSTPROCESSINGS_FIELD_NUMBER: _ClassVar[int]
    postprocessings: _containers.RepeatedCompositeFieldContainer[PostProcessing]
    def __init__(self, postprocessings: _Optional[_Iterable[_Union[PostProcessing, _Mapping]]] = ...) -> None: ...

class LabelsOutput(_message.Message):
    __slots__ = ("labels", "exclusive", "roi")
    class ROIType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[LabelsOutput.ROIType]
        BBOX: _ClassVar[LabelsOutput.ROIType]
        MASK: _ClassVar[LabelsOutput.ROIType]
    NONE: LabelsOutput.ROIType
    BBOX: LabelsOutput.ROIType
    MASK: LabelsOutput.ROIType
    class Label(_message.Message):
        __slots__ = ("id", "name")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    LABELS_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    ROI_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[LabelsOutput.Label]
    exclusive: bool
    roi: LabelsOutput.ROIType
    def __init__(self, labels: _Optional[_Iterable[_Union[LabelsOutput.Label, _Mapping]]] = ..., exclusive: bool = ..., roi: _Optional[_Union[LabelsOutput.ROIType, str]] = ...) -> None: ...

class TextOutput(_message.Message):
    __slots__ = ("characters",)
    CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    characters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, characters: _Optional[_Iterable[str]] = ...) -> None: ...

class TensorsOutput(_message.Message):
    __slots__ = ("tensors",)
    class TensorSpec(_message.Message):
        __slots__ = ("name", "shape")
        NAME_FIELD_NUMBER: _ClassVar[int]
        SHAPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        shape: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, name: _Optional[str] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    tensors: _containers.RepeatedCompositeFieldContainer[TensorsOutput.TensorSpec]
    def __init__(self, tensors: _Optional[_Iterable[_Union[TensorsOutput.TensorSpec, _Mapping]]] = ...) -> None: ...

class Outputs(_message.Message):
    __slots__ = ("outputs",)
    class OutputMix(_message.Message):
        __slots__ = ("labels", "text", "tensors")
        LABELS_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        TENSORS_FIELD_NUMBER: _ClassVar[int]
        labels: LabelsOutput
        text: TextOutput
        tensors: TensorsOutput
        def __init__(self, labels: _Optional[_Union[LabelsOutput, _Mapping]] = ..., text: _Optional[_Union[TextOutput, _Mapping]] = ..., tensors: _Optional[_Union[TensorsOutput, _Mapping]] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedCompositeFieldContainer[Outputs.OutputMix]
    def __init__(self, outputs: _Optional[_Iterable[_Union[Outputs.OutputMix, _Mapping]]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Classification(_message.Message):
    __slots__ = ("output_tensor", "thresholds")
    OUTPUT_TENSOR_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    output_tensor: str
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, output_tensor: _Optional[str] = ..., thresholds: _Optional[_Iterable[float]] = ...) -> None: ...

class Detection(_message.Message):
    __slots__ = ("output_mix", "thresholds", "nms_threshold", "discard_threshold", "normalize_wrt_tensor")
    class OutputMix(_message.Message):
        __slots__ = ("anchored_output", "direct_output", "yolo_output", "yolov3_output", "standard_output")
        ANCHORED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        DIRECT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        YOLO_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        YOLOV3_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        STANDARD_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        anchored_output: AnchoredOutput
        direct_output: DirectOutput
        yolo_output: YoloOutput
        yolov3_output: YoloV3Output
        standard_output: StandardOutput
        def __init__(self, anchored_output: _Optional[_Union[AnchoredOutput, _Mapping]] = ..., direct_output: _Optional[_Union[DirectOutput, _Mapping]] = ..., yolo_output: _Optional[_Union[YoloOutput, _Mapping]] = ..., yolov3_output: _Optional[_Union[YoloV3Output, _Mapping]] = ..., standard_output: _Optional[_Union[StandardOutput, _Mapping]] = ...) -> None: ...
    OUTPUT_MIX_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    NMS_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    DISCARD_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    NORMALIZE_WRT_TENSOR_FIELD_NUMBER: _ClassVar[int]
    output_mix: Detection.OutputMix
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    nms_threshold: float
    discard_threshold: float
    normalize_wrt_tensor: str
    def __init__(self, output_mix: _Optional[_Union[Detection.OutputMix, _Mapping]] = ..., thresholds: _Optional[_Iterable[float]] = ..., nms_threshold: _Optional[float] = ..., discard_threshold: _Optional[float] = ..., normalize_wrt_tensor: _Optional[str] = ...) -> None: ...

class OCR(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Segmentation(_message.Message):
    __slots__ = ("output_mix", "thresholds", "discard_threshold")
    class OutputMix(_message.Message):
        __slots__ = ("instance_segmentation_output",)
        INSTANCE_SEGMENTATION_OUTPUT_FIELD_NUMBER: _ClassVar[int]
        instance_segmentation_output: InstanceSegmentationOutput
        def __init__(self, instance_segmentation_output: _Optional[_Union[InstanceSegmentationOutput, _Mapping]] = ...) -> None: ...
    OUTPUT_MIX_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    DISCARD_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    output_mix: Segmentation.OutputMix
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    discard_threshold: float
    def __init__(self, output_mix: _Optional[_Union[Segmentation.OutputMix, _Mapping]] = ..., thresholds: _Optional[_Iterable[float]] = ..., discard_threshold: _Optional[float] = ...) -> None: ...

class PostprocessingsDeprecated(_message.Message):
    __slots__ = ("postprocessings",)
    class PostprocessingMixDeprecated(_message.Message):
        __slots__ = ("classification", "detection", "ocr", "segmentation", "tensors")
        CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
        DETECTION_FIELD_NUMBER: _ClassVar[int]
        OCR_FIELD_NUMBER: _ClassVar[int]
        SEGMENTATION_FIELD_NUMBER: _ClassVar[int]
        TENSORS_FIELD_NUMBER: _ClassVar[int]
        classification: Classification
        detection: Detection
        ocr: OCR
        segmentation: Segmentation
        tensors: Empty
        def __init__(self, classification: _Optional[_Union[Classification, _Mapping]] = ..., detection: _Optional[_Union[Detection, _Mapping]] = ..., ocr: _Optional[_Union[OCR, _Mapping]] = ..., segmentation: _Optional[_Union[Segmentation, _Mapping]] = ..., tensors: _Optional[_Union[Empty, _Mapping]] = ...) -> None: ...
    POSTPROCESSINGS_FIELD_NUMBER: _ClassVar[int]
    postprocessings: _containers.RepeatedCompositeFieldContainer[PostprocessingsDeprecated.PostprocessingMixDeprecated]
    def __init__(self, postprocessings: _Optional[_Iterable[_Union[PostprocessingsDeprecated.PostprocessingMixDeprecated, _Mapping]]] = ...) -> None: ...
