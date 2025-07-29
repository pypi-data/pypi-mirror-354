from buffers.protobuf.workflows import Workflow_pb2 as _Workflow_pb2
from buffers.protobuf.common import Error_pb2 as _Error_pb2
from buffers.protobuf.workflows import WorkOrder_pb2 as _WorkOrder_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkflowRequest(_message.Message):
    __slots__ = ("workflow_entries", "metadata", "output_routing_key", "return_flow_container", "return_flow_container_without_images", "wo_data", "analysis_metadata", "task_group_name", "extra_data")
    class WorkflowEntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _Workflow_pb2.Concept
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_Workflow_pb2.Concept, _Mapping]] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class AnalysisMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    WORKFLOW_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ROUTING_KEY_FIELD_NUMBER: _ClassVar[int]
    RETURN_FLOW_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    RETURN_FLOW_CONTAINER_WITHOUT_IMAGES_FIELD_NUMBER: _ClassVar[int]
    WO_DATA_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_METADATA_FIELD_NUMBER: _ClassVar[int]
    TASK_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
    workflow_entries: _containers.MessageMap[str, _Workflow_pb2.Concept]
    metadata: _containers.ScalarMap[str, str]
    output_routing_key: str
    return_flow_container: bool
    return_flow_container_without_images: bool
    wo_data: _WorkOrder_pb2.WorkOrderData
    analysis_metadata: _containers.ScalarMap[str, str]
    task_group_name: str
    extra_data: str
    def __init__(self, workflow_entries: _Optional[_Mapping[str, _Workflow_pb2.Concept]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., output_routing_key: _Optional[str] = ..., return_flow_container: bool = ..., return_flow_container_without_images: bool = ..., wo_data: _Optional[_Union[_WorkOrder_pb2.WorkOrderData, _Mapping]] = ..., analysis_metadata: _Optional[_Mapping[str, str]] = ..., task_group_name: _Optional[str] = ..., extra_data: _Optional[str] = ...) -> None: ...

class WorkflowResponse(_message.Message):
    __slots__ = ("error", "outcomes", "flow_container", "analysis_id")
    class OutcomesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _Workflow_pb2.Outcome
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_Workflow_pb2.Outcome, _Mapping]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_ID_FIELD_NUMBER: _ClassVar[int]
    error: _Error_pb2.Error
    outcomes: _containers.MessageMap[str, _Workflow_pb2.Outcome]
    flow_container: _Workflow_pb2.FlowContainer
    analysis_id: str
    def __init__(self, error: _Optional[_Union[_Error_pb2.Error, _Mapping]] = ..., outcomes: _Optional[_Mapping[str, _Workflow_pb2.Outcome]] = ..., flow_container: _Optional[_Union[_Workflow_pb2.FlowContainer, _Mapping]] = ..., analysis_id: _Optional[str] = ...) -> None: ...
