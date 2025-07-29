from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from models import graph_models_pb2 as _graph_models_pb2
from models import ai_models_pb2 as _ai_models_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InferenceRequest(_message.Message):
    __slots__ = ["camera", "frame", "image_data", "timestamp"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    camera: _graph_models_pb2.Camera
    frame: _ai_models_pb2.InferenceFrame
    image_data: bytes
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., image_data: _Optional[bytes] = ...) -> None: ...
