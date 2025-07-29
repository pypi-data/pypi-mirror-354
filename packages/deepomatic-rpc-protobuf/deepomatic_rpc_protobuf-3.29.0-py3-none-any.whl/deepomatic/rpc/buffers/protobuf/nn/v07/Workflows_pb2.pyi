from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Consumer(_message.Message):
    __slots__ = ("amqp",)
    class AMQP(_message.Message):
        __slots__ = ("exchange", "queue")
        EXCHANGE_FIELD_NUMBER: _ClassVar[int]
        QUEUE_FIELD_NUMBER: _ClassVar[int]
        exchange: str
        queue: str
        def __init__(self, exchange: _Optional[str] = ..., queue: _Optional[str] = ...) -> None: ...
    AMQP_FIELD_NUMBER: _ClassVar[int]
    amqp: Consumer.AMQP
    def __init__(self, amqp: _Optional[_Union[Consumer.AMQP, _Mapping]] = ...) -> None: ...

class Transformation(_message.Message):
    __slots__ = ("network", "recognition")
    class Network(_message.Message):
        __slots__ = ("network_id",)
        NETWORK_ID_FIELD_NUMBER: _ClassVar[int]
        network_id: int
        def __init__(self, network_id: _Optional[int] = ...) -> None: ...
    class Recognition(_message.Message):
        __slots__ = ("recognition_id",)
        RECOGNITION_ID_FIELD_NUMBER: _ClassVar[int]
        recognition_id: int
        def __init__(self, recognition_id: _Optional[int] = ...) -> None: ...
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    RECOGNITION_FIELD_NUMBER: _ClassVar[int]
    network: Transformation.Network
    recognition: Transformation.Recognition
    def __init__(self, network: _Optional[_Union[Transformation.Network, _Mapping]] = ..., recognition: _Optional[_Union[Transformation.Recognition, _Mapping]] = ...) -> None: ...

class Workflow(_message.Message):
    __slots__ = ("name", "consumer", "transformations")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    consumer: Consumer
    transformations: _containers.RepeatedCompositeFieldContainer[Transformation]
    def __init__(self, name: _Optional[str] = ..., consumer: _Optional[_Union[Consumer, _Mapping]] = ..., transformations: _Optional[_Iterable[_Union[Transformation, _Mapping]]] = ...) -> None: ...

class Workflows(_message.Message):
    __slots__ = ("workflows",)
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    workflows: _containers.RepeatedCompositeFieldContainer[Workflow]
    def __init__(self, workflows: _Optional[_Iterable[_Union[Workflow, _Mapping]]] = ...) -> None: ...
