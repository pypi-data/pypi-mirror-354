from buffers.protobuf.nn.v07 import Commands_pb2 as _Commands_pb2
from buffers.protobuf.nn.v07 import Inputs_pb2 as _Inputs_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandMix(_message.Message):
    __slots__ = ("v07_inference", "v07_recognition", "v07_workflow")
    V07_INFERENCE_FIELD_NUMBER: _ClassVar[int]
    V07_RECOGNITION_FIELD_NUMBER: _ClassVar[int]
    V07_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    v07_inference: _Commands_pb2.Inference
    v07_recognition: _Commands_pb2.Recognition
    v07_workflow: _Commands_pb2.Workflow
    def __init__(self, v07_inference: _Optional[_Union[_Commands_pb2.Inference, _Mapping]] = ..., v07_recognition: _Optional[_Union[_Commands_pb2.Recognition, _Mapping]] = ..., v07_workflow: _Optional[_Union[_Commands_pb2.Workflow, _Mapping]] = ...) -> None: ...

class InputMix(_message.Message):
    __slots__ = ("v07_inputs",)
    V07_INPUTS_FIELD_NUMBER: _ClassVar[int]
    v07_inputs: _Inputs_pb2.Inputs
    def __init__(self, v07_inputs: _Optional[_Union[_Inputs_pb2.Inputs, _Mapping]] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CommandInfo(_message.Message):
    __slots__ = ("app_id", "app_pk", "track_id", "date_plan", "current_queue", "forward_to")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_PK_FIELD_NUMBER: _ClassVar[int]
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_PLAN_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QUEUE_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TO_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    app_pk: int
    track_id: str
    date_plan: str
    current_queue: int
    forward_to: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app_id: _Optional[str] = ..., app_pk: _Optional[int] = ..., track_id: _Optional[str] = ..., date_plan: _Optional[str] = ..., current_queue: _Optional[int] = ..., forward_to: _Optional[_Iterable[str]] = ...) -> None: ...

class Command(_message.Message):
    __slots__ = ("task", "base_info", "command_mix", "input_mix")
    TASK_FIELD_NUMBER: _ClassVar[int]
    BASE_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMAND_MIX_FIELD_NUMBER: _ClassVar[int]
    INPUT_MIX_FIELD_NUMBER: _ClassVar[int]
    task: Task
    base_info: CommandInfo
    command_mix: CommandMix
    input_mix: InputMix
    def __init__(self, task: _Optional[_Union[Task, _Mapping]] = ..., base_info: _Optional[_Union[CommandInfo, _Mapping]] = ..., command_mix: _Optional[_Union[CommandMix, _Mapping]] = ..., input_mix: _Optional[_Union[InputMix, _Mapping]] = ...) -> None: ...
