from buffers.protobuf.common import Image_pb2 as _Image_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageInput(_message.Message):
    __slots__ = ("source", "bbox", "polygon", "crop_uniform_background")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    BBOX_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    CROP_UNIFORM_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    source: bytes
    bbox: _Image_pb2.BBox
    polygon: _containers.RepeatedCompositeFieldContainer[_Image_pb2.Point]
    crop_uniform_background: bool
    def __init__(self, source: _Optional[bytes] = ..., bbox: _Optional[_Union[_Image_pb2.BBox, _Mapping]] = ..., polygon: _Optional[_Iterable[_Union[_Image_pb2.Point, _Mapping]]] = ..., crop_uniform_background: bool = ...) -> None: ...

class Inputs(_message.Message):
    __slots__ = ("inputs",)
    class InputMix(_message.Message):
        __slots__ = ("image",)
        IMAGE_FIELD_NUMBER: _ClassVar[int]
        image: ImageInput
        def __init__(self, image: _Optional[_Union[ImageInput, _Mapping]] = ...) -> None: ...
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[Inputs.InputMix]
    def __init__(self, inputs: _Optional[_Iterable[_Union[Inputs.InputMix, _Mapping]]] = ...) -> None: ...
