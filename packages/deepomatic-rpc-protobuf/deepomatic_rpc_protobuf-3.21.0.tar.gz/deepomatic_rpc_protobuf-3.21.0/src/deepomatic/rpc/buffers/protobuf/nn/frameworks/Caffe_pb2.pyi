from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlobShape(_message.Message):
    __slots__ = ("dim",)
    DIM_FIELD_NUMBER: _ClassVar[int]
    dim: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dim: _Optional[_Iterable[int]] = ...) -> None: ...

class BlobProto(_message.Message):
    __slots__ = ("shape", "data", "diff", "double_data", "double_diff", "num", "channels", "height", "width")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_DATA_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_DIFF_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    shape: BlobShape
    data: _containers.RepeatedScalarFieldContainer[float]
    diff: _containers.RepeatedScalarFieldContainer[float]
    double_data: _containers.RepeatedScalarFieldContainer[float]
    double_diff: _containers.RepeatedScalarFieldContainer[float]
    num: int
    channels: int
    height: int
    width: int
    def __init__(self, shape: _Optional[_Union[BlobShape, _Mapping]] = ..., data: _Optional[_Iterable[float]] = ..., diff: _Optional[_Iterable[float]] = ..., double_data: _Optional[_Iterable[float]] = ..., double_diff: _Optional[_Iterable[float]] = ..., num: _Optional[int] = ..., channels: _Optional[int] = ..., height: _Optional[int] = ..., width: _Optional[int] = ...) -> None: ...
