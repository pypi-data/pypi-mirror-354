from buffers.protobuf.common import Image_pb2 as _Image_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inference(_message.Message):
    __slots__ = ("tensors",)
    class Tensor(_message.Message):
        __slots__ = ("shape", "data", "name")
        SHAPE_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        shape: _containers.RepeatedScalarFieldContainer[int]
        data: _containers.RepeatedScalarFieldContainer[float]
        name: str
        def __init__(self, shape: _Optional[_Iterable[int]] = ..., data: _Optional[_Iterable[float]] = ..., name: _Optional[str] = ...) -> None: ...
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    tensors: _containers.RepeatedCompositeFieldContainer[Inference.Tensor]
    def __init__(self, tensors: _Optional[_Iterable[_Union[Inference.Tensor, _Mapping]]] = ...) -> None: ...

class Mask(_message.Message):
    __slots__ = ("bbox", "polygons")
    BBOX_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    bbox: _Image_pb2.BBox
    polygons: _containers.RepeatedCompositeFieldContainer[_Image_pb2.Polygon]
    def __init__(self, bbox: _Optional[_Union[_Image_pb2.BBox, _Mapping]] = ..., polygons: _Optional[_Iterable[_Union[_Image_pb2.Polygon, _Mapping]]] = ...) -> None: ...

class ROI(_message.Message):
    __slots__ = ("region_id", "bbox", "mask")
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    region_id: int
    bbox: _Image_pb2.BBox
    mask: Mask
    def __init__(self, region_id: _Optional[int] = ..., bbox: _Optional[_Union[_Image_pb2.BBox, _Mapping]] = ..., mask: _Optional[_Union[Mask, _Mapping]] = ...) -> None: ...

class LabelsOutput(_message.Message):
    __slots__ = ("predicted", "discarded")
    class Prediction(_message.Message):
        __slots__ = ("label_id", "label_name", "score", "threshold", "roi")
        LABEL_ID_FIELD_NUMBER: _ClassVar[int]
        LABEL_NAME_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        ROI_FIELD_NUMBER: _ClassVar[int]
        label_id: int
        label_name: str
        score: float
        threshold: float
        roi: ROI
        def __init__(self, label_id: _Optional[int] = ..., label_name: _Optional[str] = ..., score: _Optional[float] = ..., threshold: _Optional[float] = ..., roi: _Optional[_Union[ROI, _Mapping]] = ...) -> None: ...
    PREDICTED_FIELD_NUMBER: _ClassVar[int]
    DISCARDED_FIELD_NUMBER: _ClassVar[int]
    predicted: _containers.RepeatedCompositeFieldContainer[LabelsOutput.Prediction]
    discarded: _containers.RepeatedCompositeFieldContainer[LabelsOutput.Prediction]
    def __init__(self, predicted: _Optional[_Iterable[_Union[LabelsOutput.Prediction, _Mapping]]] = ..., discarded: _Optional[_Iterable[_Union[LabelsOutput.Prediction, _Mapping]]] = ...) -> None: ...

class ScalarOutput(_message.Message):
    __slots__ = ("integer",)
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    integer: int
    def __init__(self, integer: _Optional[int] = ...) -> None: ...

class TextOutput(_message.Message):
    __slots__ = ("text", "mean_score", "tokens", "scores")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    MEAN_SCORE_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    text: str
    mean_score: float
    tokens: _containers.RepeatedScalarFieldContainer[str]
    scores: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, text: _Optional[str] = ..., mean_score: _Optional[float] = ..., tokens: _Optional[_Iterable[str]] = ..., scores: _Optional[_Iterable[float]] = ...) -> None: ...

class RecognitionMix(_message.Message):
    __slots__ = ("labels", "scalar", "text", "tensors")
    LABELS_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    labels: LabelsOutput
    scalar: ScalarOutput
    text: TextOutput
    tensors: Inference
    def __init__(self, labels: _Optional[_Union[LabelsOutput, _Mapping]] = ..., scalar: _Optional[_Union[ScalarOutput, _Mapping]] = ..., text: _Optional[_Union[TextOutput, _Mapping]] = ..., tensors: _Optional[_Union[Inference, _Mapping]] = ...) -> None: ...

class Recognition(_message.Message):
    __slots__ = ("outputs",)
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedCompositeFieldContainer[RecognitionMix]
    def __init__(self, outputs: _Optional[_Iterable[_Union[RecognitionMix, _Mapping]]] = ...) -> None: ...
