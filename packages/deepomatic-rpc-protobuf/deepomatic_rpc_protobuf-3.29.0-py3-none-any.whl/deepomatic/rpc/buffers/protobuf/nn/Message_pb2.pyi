from buffers.protobuf.nn import Command_pb2 as _Command_pb2
from buffers.protobuf.nn import Result_pb2 as _Result_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("command", "result")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    command: _Command_pb2.Command
    result: _Result_pb2.Result
    def __init__(self, command: _Optional[_Union[_Command_pb2.Command, _Mapping]] = ..., result: _Optional[_Union[_Result_pb2.Result, _Mapping]] = ...) -> None: ...
