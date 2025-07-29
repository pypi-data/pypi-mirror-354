from google.protobuf import timestamp_pb2 as _timestamp_pb2
from models import ai_models_pb2 as _ai_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RenderingDetectedObjectAttributes(_message.Message):
    __slots__ = ["state", "track_id"]
    class RenderingDetectedObjectState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    NORMAL: RenderingDetectedObjectAttributes.RenderingDetectedObjectState
    OBJECT_NEEDS_ATTENTION: RenderingDetectedObjectAttributes.RenderingDetectedObjectState
    OBJECT_OF_INTEREST: RenderingDetectedObjectAttributes.RenderingDetectedObjectState
    STATE_FIELD_NUMBER: _ClassVar[int]
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: RenderingDetectedObjectAttributes.RenderingDetectedObjectState
    state: RenderingDetectedObjectAttributes.RenderingDetectedObjectState
    track_id: str
    def __init__(self, track_id: _Optional[str] = ..., state: _Optional[_Union[RenderingDetectedObjectAttributes.RenderingDetectedObjectState, str]] = ...) -> None: ...

class RenderingFrame(_message.Message):
    __slots__ = ["detected_objects", "detected_objects_attributes", "facility_id", "id", "level_id", "location_attributes", "timestamp"]
    DETECTED_OBJECTS_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    DETECTED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    detected_objects: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.DetectedObject]
    detected_objects_attributes: _containers.RepeatedCompositeFieldContainer[RenderingDetectedObjectAttributes]
    facility_id: str
    id: str
    level_id: str
    location_attributes: _containers.RepeatedCompositeFieldContainer[RenderingLocationAttributes]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., facility_id: _Optional[str] = ..., level_id: _Optional[str] = ..., detected_objects: _Optional[_Iterable[_Union[_ai_models_pb2.DetectedObject, _Mapping]]] = ..., location_attributes: _Optional[_Iterable[_Union[RenderingLocationAttributes, _Mapping]]] = ..., detected_objects_attributes: _Optional[_Iterable[_Union[RenderingDetectedObjectAttributes, _Mapping]]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RenderingLocationAttributes(_message.Message):
    __slots__ = ["location_id", "state"]
    class RenderingLocationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    INCIDENT_IN_PROGRESS: RenderingLocationAttributes.RenderingLocationState
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_NEEDS_ATTENTION: RenderingLocationAttributes.RenderingLocationState
    NORMAL: RenderingLocationAttributes.RenderingLocationState
    STATE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: RenderingLocationAttributes.RenderingLocationState
    location_id: str
    state: RenderingLocationAttributes.RenderingLocationState
    def __init__(self, location_id: _Optional[str] = ..., state: _Optional[_Union[RenderingLocationAttributes.RenderingLocationState, str]] = ...) -> None: ...

class SpatialCalibrationData(_message.Message):
    __slots__ = ["id", "image_coordinates", "world_coordinates"]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    WORLD_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    id: str
    image_coordinates: _containers.RepeatedCompositeFieldContainer[SpatialCoordinate]
    world_coordinates: _containers.RepeatedCompositeFieldContainer[SpatialWorldPoint]
    def __init__(self, id: _Optional[str] = ..., image_coordinates: _Optional[_Iterable[_Union[SpatialCoordinate, _Mapping]]] = ..., world_coordinates: _Optional[_Iterable[_Union[SpatialWorldPoint, _Mapping]]] = ...) -> None: ...

class SpatialCoordinate(_message.Message):
    __slots__ = ["id", "index", "x", "y"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    id: str
    index: int
    x: float
    y: float
    def __init__(self, id: _Optional[str] = ..., index: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class SpatialWorldPoint(_message.Message):
    __slots__ = ["id", "index", "x", "y", "z"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    id: str
    index: int
    x: float
    y: float
    z: float
    def __init__(self, id: _Optional[str] = ..., index: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...
