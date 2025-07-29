from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkOrderData(_message.Message):
    __slots__ = ("metadata", "states", "types")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class StatesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: WorkItemState
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[WorkItemState, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.ScalarMap[str, str]
    states: _containers.MessageMap[str, WorkItemState]
    types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metadata: _Optional[_Mapping[str, str]] = ..., states: _Optional[_Mapping[str, WorkItemState]] = ..., types: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkItemState(_message.Message):
    __slots__ = ("state_values", "memory")
    class StateValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATE_VALUES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    state_values: _containers.ScalarMap[str, str]
    memory: str
    def __init__(self, state_values: _Optional[_Mapping[str, str]] = ..., memory: _Optional[str] = ...) -> None: ...
