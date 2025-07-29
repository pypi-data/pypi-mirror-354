from google.protobuf import timestamp_pb2 as _timestamp_pb2
from models import ai_models_pb2 as _ai_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OccupancyCount(_message.Message):
    __slots__ = ["cameraId", "contextId", "count", "detectedObjects", "facilityId", "id", "levelId", "locationId", "timestamp", "zoneId"]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    CONTEXTID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DETECTEDOBJECTS_FIELD_NUMBER: _ClassVar[int]
    FACILITYID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVELID_FIELD_NUMBER: _ClassVar[int]
    LOCATIONID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ZONEID_FIELD_NUMBER: _ClassVar[int]
    cameraId: str
    contextId: str
    count: int
    detectedObjects: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.DetectedObject]
    facilityId: str
    id: str
    levelId: str
    locationId: str
    timestamp: _timestamp_pb2.Timestamp
    zoneId: str
    def __init__(self, id: _Optional[str] = ..., contextId: _Optional[str] = ..., count: _Optional[int] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cameraId: _Optional[str] = ..., locationId: _Optional[str] = ..., levelId: _Optional[str] = ..., facilityId: _Optional[str] = ..., zoneId: _Optional[str] = ..., detectedObjects: _Optional[_Iterable[_Union[_ai_models_pb2.DetectedObject, _Mapping]]] = ...) -> None: ...
