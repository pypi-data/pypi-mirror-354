from google.protobuf import empty_pb2 as _empty_pb2
from models import graph_models_pb2 as _graph_models_pb2
from models import service_models_pb2 as _service_models_pb2
from models import ai_models_pb2 as _ai_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FrameThroughput(_message.Message):
    __slots__ = ["camera_id", "number_of_message"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    number_of_message: int
    def __init__(self, camera_id: _Optional[str] = ..., number_of_message: _Optional[int] = ...) -> None: ...

class IncidentPrompt(_message.Message):
    __slots__ = ["debug_cropped_frame", "frame_count", "frame_ids", "incident_id", "prompt"]
    DEBUG_CROPPED_FRAME_FIELD_NUMBER: _ClassVar[int]
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRAME_IDS_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    debug_cropped_frame: bool
    frame_count: int
    frame_ids: _containers.RepeatedScalarFieldContainer[str]
    incident_id: str
    prompt: str
    def __init__(self, incident_id: _Optional[str] = ..., prompt: _Optional[str] = ..., frame_count: _Optional[int] = ..., debug_cropped_frame: bool = ..., frame_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class IncidentPromptResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
