from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeanTensor(_message.Message):
    __slots__ = ("shape", "data")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...

class ConstantPreprocessing(_message.Message):
    __slots__ = ("shape", "data")
    class Entry(_message.Message):
        __slots__ = ("float_entry", "string_entry")
        FLOAT_ENTRY_FIELD_NUMBER: _ClassVar[int]
        STRING_ENTRY_FIELD_NUMBER: _ClassVar[int]
        float_entry: float
        string_entry: str
        def __init__(self, float_entry: _Optional[float] = ..., string_entry: _Optional[str] = ...) -> None: ...
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    data: _containers.RepeatedCompositeFieldContainer[ConstantPreprocessing.Entry]
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., data: _Optional[_Iterable[_Union[ConstantPreprocessing.Entry, _Mapping]]] = ...) -> None: ...

class ImagePreprocessing(_message.Message):
    __slots__ = ("mean_file", "color_channels", "dimension_order", "resize_type", "target_size", "pixel_scaling", "data_type")
    class ResizeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NETWORK: _ClassVar[ImagePreprocessing.ResizeType]
        FILL: _ClassVar[ImagePreprocessing.ResizeType]
        CROP: _ClassVar[ImagePreprocessing.ResizeType]
        SQUASH: _ClassVar[ImagePreprocessing.ResizeType]
    NETWORK: ImagePreprocessing.ResizeType
    FILL: ImagePreprocessing.ResizeType
    CROP: ImagePreprocessing.ResizeType
    SQUASH: ImagePreprocessing.ResizeType
    class ColorChannels(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BGR: _ClassVar[ImagePreprocessing.ColorChannels]
        RGB: _ClassVar[ImagePreprocessing.ColorChannels]
        GRAY: _ClassVar[ImagePreprocessing.ColorChannels]
    BGR: ImagePreprocessing.ColorChannels
    RGB: ImagePreprocessing.ColorChannels
    GRAY: ImagePreprocessing.ColorChannels
    class DimensionOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NCHW: _ClassVar[ImagePreprocessing.DimensionOrder]
        NCWH: _ClassVar[ImagePreprocessing.DimensionOrder]
        NHWC: _ClassVar[ImagePreprocessing.DimensionOrder]
        NWHC: _ClassVar[ImagePreprocessing.DimensionOrder]
    NCHW: ImagePreprocessing.DimensionOrder
    NCWH: ImagePreprocessing.DimensionOrder
    NHWC: ImagePreprocessing.DimensionOrder
    NWHC: ImagePreprocessing.DimensionOrder
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FLOAT32: _ClassVar[ImagePreprocessing.DataType]
        UINT8: _ClassVar[ImagePreprocessing.DataType]
    FLOAT32: ImagePreprocessing.DataType
    UINT8: ImagePreprocessing.DataType
    MEAN_FILE_FIELD_NUMBER: _ClassVar[int]
    COLOR_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_ORDER_FIELD_NUMBER: _ClassVar[int]
    RESIZE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_SIZE_FIELD_NUMBER: _ClassVar[int]
    PIXEL_SCALING_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    mean_file: str
    color_channels: ImagePreprocessing.ColorChannels
    dimension_order: ImagePreprocessing.DimensionOrder
    resize_type: ImagePreprocessing.ResizeType
    target_size: str
    pixel_scaling: float
    data_type: ImagePreprocessing.DataType
    def __init__(self, mean_file: _Optional[str] = ..., color_channels: _Optional[_Union[ImagePreprocessing.ColorChannels, str]] = ..., dimension_order: _Optional[_Union[ImagePreprocessing.DimensionOrder, str]] = ..., resize_type: _Optional[_Union[ImagePreprocessing.ResizeType, str]] = ..., target_size: _Optional[str] = ..., pixel_scaling: _Optional[float] = ..., data_type: _Optional[_Union[ImagePreprocessing.DataType, str]] = ...) -> None: ...

class PreprocessingMix(_message.Message):
    __slots__ = ("constant", "image")
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    constant: ConstantPreprocessing
    image: ImagePreprocessing
    def __init__(self, constant: _Optional[_Union[ConstantPreprocessing, _Mapping]] = ..., image: _Optional[_Union[ImagePreprocessing, _Mapping]] = ...) -> None: ...

class Preprocessing(_message.Message):
    __slots__ = ("tensor_name", "preprocessing_mix")
    TENSOR_NAME_FIELD_NUMBER: _ClassVar[int]
    PREPROCESSING_MIX_FIELD_NUMBER: _ClassVar[int]
    tensor_name: str
    preprocessing_mix: PreprocessingMix
    def __init__(self, tensor_name: _Optional[str] = ..., preprocessing_mix: _Optional[_Union[PreprocessingMix, _Mapping]] = ...) -> None: ...

class Preprocessings(_message.Message):
    __slots__ = ("inputs", "batched_output")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    BATCHED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[Preprocessing]
    batched_output: bool
    def __init__(self, inputs: _Optional[_Iterable[_Union[Preprocessing, _Mapping]]] = ..., batched_output: bool = ...) -> None: ...
