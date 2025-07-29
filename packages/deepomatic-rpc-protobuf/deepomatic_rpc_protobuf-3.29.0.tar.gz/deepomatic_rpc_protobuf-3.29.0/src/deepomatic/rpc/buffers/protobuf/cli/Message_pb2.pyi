from buffers.protobuf.nn import Command_pb2 as _Command_pb2
from buffers.protobuf.nn import Result_pb2 as _Result_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ("command_mix", "input_mix")
    COMMAND_MIX_FIELD_NUMBER: _ClassVar[int]
    INPUT_MIX_FIELD_NUMBER: _ClassVar[int]
    command_mix: _Command_pb2.CommandMix
    input_mix: _Command_pb2.InputMix
    def __init__(self, command_mix: _Optional[_Union[_Command_pb2.CommandMix, _Mapping]] = ..., input_mix: _Optional[_Union[_Command_pb2.InputMix, _Mapping]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("command", "result")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    command: Command
    result: _Result_pb2.Result
    def __init__(self, command: _Optional[_Union[Command, _Mapping]] = ..., result: _Optional[_Union[_Result_pb2.Result, _Mapping]] = ...) -> None: ...
