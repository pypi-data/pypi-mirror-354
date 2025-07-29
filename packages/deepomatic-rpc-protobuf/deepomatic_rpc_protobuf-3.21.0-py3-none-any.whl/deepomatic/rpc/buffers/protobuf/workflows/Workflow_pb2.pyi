from buffers.protobuf.nn.v07 import Results_pb2 as _Results_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Predictions(_message.Message):
    __slots__ = ("predictions",)
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[Prediction]
    def __init__(self, predictions: _Optional[_Iterable[_Union[Prediction, _Mapping]]] = ...) -> None: ...

class Prediction(_message.Message):
    __slots__ = ("label_id", "label_name", "score")
    LABEL_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    label_id: int
    label_name: str
    score: float
    def __init__(self, label_id: _Optional[int] = ..., label_name: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ("filename", "content", "mime_type")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content: bytes
    mime_type: str
    def __init__(self, filename: _Optional[str] = ..., content: _Optional[bytes] = ..., mime_type: _Optional[str] = ...) -> None: ...

class Concept(_message.Message):
    __slots__ = ("image", "text", "number", "predictions", "region", "boolean", "file")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    text: str
    number: float
    predictions: Predictions
    region: Region
    boolean: bool
    file: File
    def __init__(self, image: _Optional[bytes] = ..., text: _Optional[str] = ..., number: _Optional[float] = ..., predictions: _Optional[_Union[Predictions, _Mapping]] = ..., region: _Optional[_Union[Region, _Mapping]] = ..., boolean: bool = ..., file: _Optional[_Union[File, _Mapping]] = ...) -> None: ...

class Region(_message.Message):
    __slots__ = ("roi", "concepts", "entry_name")
    class ConceptsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Concept
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Concept, _Mapping]] = ...) -> None: ...
    ROI_FIELD_NUMBER: _ClassVar[int]
    CONCEPTS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    roi: _Results_pb2.ROI
    concepts: _containers.MessageMap[str, Concept]
    entry_name: str
    def __init__(self, roi: _Optional[_Union[_Results_pb2.ROI, _Mapping]] = ..., concepts: _Optional[_Mapping[str, Concept]] = ..., entry_name: _Optional[str] = ...) -> None: ...

class WorkflowDataItem(_message.Message):
    __slots__ = ("entry", "regions")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    REGIONS_FIELD_NUMBER: _ClassVar[int]
    entry: Concept
    regions: _containers.RepeatedCompositeFieldContainer[Region]
    def __init__(self, entry: _Optional[_Union[Concept, _Mapping]] = ..., regions: _Optional[_Iterable[_Union[Region, _Mapping]]] = ...) -> None: ...

class FlowContainer(_message.Message):
    __slots__ = ("workflow_data", "metadata")
    class WorkflowDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: WorkflowDataItem
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[WorkflowDataItem, _Mapping]] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    WORKFLOW_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    workflow_data: _containers.MessageMap[str, WorkflowDataItem]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, workflow_data: _Optional[_Mapping[str, WorkflowDataItem]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Outcome(_message.Message):
    __slots__ = ("concepts", "regions")
    CONCEPTS_FIELD_NUMBER: _ClassVar[int]
    REGIONS_FIELD_NUMBER: _ClassVar[int]
    concepts: _containers.RepeatedCompositeFieldContainer[Concept]
    regions: _containers.RepeatedCompositeFieldContainer[Region]
    def __init__(self, concepts: _Optional[_Iterable[_Union[Concept, _Mapping]]] = ..., regions: _Optional[_Iterable[_Union[Region, _Mapping]]] = ...) -> None: ...
