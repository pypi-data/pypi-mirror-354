from buffers.protobuf.common import Error_pb2 as _Error_pb2
from buffers.protobuf.nn.v07 import Results_pb2 as _Results_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Result(_message.Message):
    __slots__ = ("error", "v07_inference", "v07_recognition")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    V07_INFERENCE_FIELD_NUMBER: _ClassVar[int]
    V07_RECOGNITION_FIELD_NUMBER: _ClassVar[int]
    error: _Error_pb2.Error
    v07_inference: _Results_pb2.Inference
    v07_recognition: _Results_pb2.Recognition
    def __init__(self, error: _Optional[_Union[_Error_pb2.Error, _Mapping]] = ..., v07_inference: _Optional[_Union[_Results_pb2.Inference, _Mapping]] = ..., v07_recognition: _Optional[_Union[_Results_pb2.Recognition, _Mapping]] = ...) -> None: ...
