from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

BADGE_READER: EntityProtoType
CAMERA: EntityProtoType
CUSTOMER: EntityProtoType
DESCRIPTOR: _descriptor.FileDescriptor
FACILITY: EntityProtoType
GLOBAL: EntityProtoType
OBJECT: EntityProtoType
VAPE_DETECTOR: EntityProtoType
ZONE: EntityProtoType

class EntityProto(_message.Message):
    __slots__ = ["entityType", "id"]
    ENTITYTYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    entityType: EntityProtoType
    id: str
    def __init__(self, id: _Optional[str] = ..., entityType: _Optional[_Union[EntityProtoType, str]] = ...) -> None: ...

class FeatureKey(_message.Message):
    __slots__ = ["cameraId", "facilityId", "name"]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    FACILITYID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    cameraId: str
    facilityId: str
    name: str
    def __init__(self, cameraId: _Optional[str] = ..., facilityId: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class FeatureProto(_message.Message):
    __slots__ = ["booleanValue", "bytesValue", "cameraId", "doubleValue", "entity", "facilityId", "floatValue", "intValue", "longValue", "name", "stringValue", "timestamp", "zoneId"]
    BOOLEANVALUE_FIELD_NUMBER: _ClassVar[int]
    BYTESVALUE_FIELD_NUMBER: _ClassVar[int]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FACILITYID_FIELD_NUMBER: _ClassVar[int]
    FLOATVALUE_FIELD_NUMBER: _ClassVar[int]
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    LONGVALUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRINGVALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ZONEID_FIELD_NUMBER: _ClassVar[int]
    booleanValue: bool
    bytesValue: bytes
    cameraId: str
    doubleValue: float
    entity: EntityProto
    facilityId: str
    floatValue: float
    intValue: int
    longValue: int
    name: str
    stringValue: str
    timestamp: _timestamp_pb2.Timestamp
    zoneId: str
    def __init__(self, entity: _Optional[_Union[EntityProto, _Mapping]] = ..., name: _Optional[str] = ..., stringValue: _Optional[str] = ..., intValue: _Optional[int] = ..., floatValue: _Optional[float] = ..., doubleValue: _Optional[float] = ..., booleanValue: bool = ..., longValue: _Optional[int] = ..., bytesValue: _Optional[bytes] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cameraId: _Optional[str] = ..., facilityId: _Optional[str] = ..., zoneId: _Optional[str] = ...) -> None: ...

class FeatureProtoList(_message.Message):
    __slots__ = ["features"]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureProto]
    def __init__(self, features: _Optional[_Iterable[_Union[FeatureProto, _Mapping]]] = ...) -> None: ...

class EntityProtoType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
