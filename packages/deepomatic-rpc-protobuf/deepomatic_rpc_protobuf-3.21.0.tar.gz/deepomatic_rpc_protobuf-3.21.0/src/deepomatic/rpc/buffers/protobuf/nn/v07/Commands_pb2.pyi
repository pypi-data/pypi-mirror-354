from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Inference(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Recognition(_message.Message):
    __slots__ = ("version_id", "show_discarded", "max_predictions")
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    SHOW_DISCARDED_FIELD_NUMBER: _ClassVar[int]
    MAX_PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    version_id: int
    show_discarded: bool
    max_predictions: int
    def __init__(self, version_id: _Optional[int] = ..., show_discarded: bool = ..., max_predictions: _Optional[int] = ...) -> None: ...

class Workflow(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
