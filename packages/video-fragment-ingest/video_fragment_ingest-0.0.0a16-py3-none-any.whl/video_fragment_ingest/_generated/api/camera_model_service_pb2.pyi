from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ALL: LocalizationReadyStatus
DESCRIPTOR: _descriptor.FileDescriptor
NOT_READY: LocalizationReadyStatus
READY: LocalizationReadyStatus
UNKNOWN: LocalizationReadyStatus

class GetCameraManufacturersRequest(_message.Message):
    __slots__ = ["predicate"]
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    predicate: str
    def __init__(self, predicate: _Optional[str] = ...) -> None: ...

class GetCameraManufacturersResponse(_message.Message):
    __slots__ = ["manufacturers"]
    MANUFACTURERS_FIELD_NUMBER: _ClassVar[int]
    manufacturers: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.CameraManufacturer]
    def __init__(self, manufacturers: _Optional[_Iterable[_Union[_graph_models_pb2.CameraManufacturer, _Mapping]]] = ...) -> None: ...

class GetCameraModelsRequest(_message.Message):
    __slots__ = ["localization_ready_status", "manufacturer", "predicate"]
    LOCALIZATION_READY_STATUS_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    localization_ready_status: LocalizationReadyStatus
    manufacturer: _graph_models_pb2.CameraManufacturer
    predicate: str
    def __init__(self, manufacturer: _Optional[_Union[_graph_models_pb2.CameraManufacturer, _Mapping]] = ..., predicate: _Optional[str] = ..., localization_ready_status: _Optional[_Union[LocalizationReadyStatus, str]] = ...) -> None: ...

class GetCameraModelsResponse(_message.Message):
    __slots__ = ["models"]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.CameraModel]
    def __init__(self, models: _Optional[_Iterable[_Union[_graph_models_pb2.CameraModel, _Mapping]]] = ...) -> None: ...

class LocalizationReadyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
