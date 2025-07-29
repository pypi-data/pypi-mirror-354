from google.protobuf import timestamp_pb2 as _timestamp_pb2
from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeployModelRequest(_message.Message):
    __slots__ = ["config", "devices", "id"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    config: str
    devices: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Device]
    id: str
    def __init__(self, id: _Optional[str] = ..., devices: _Optional[_Iterable[_Union[_graph_models_pb2.Device, _Mapping]]] = ..., config: _Optional[str] = ...) -> None: ...

class DeployModelResponse(_message.Message):
    __slots__ = ["devices", "id"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceModelDeployResponse]
    id: str
    def __init__(self, id: _Optional[str] = ..., devices: _Optional[_Iterable[_Union[DeviceModelDeployResponse, _Mapping]]] = ...) -> None: ...

class DeviceActiveModelRequest(_message.Message):
    __slots__ = ["device_id", "id"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    id: str
    def __init__(self, id: _Optional[str] = ..., device_id: _Optional[str] = ...) -> None: ...

class DeviceActiveModelResponse(_message.Message):
    __slots__ = ["active_model_artifacts", "device_id", "id", "request_id"]
    ACTIVE_MODEL_ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    active_model_artifacts: ModelArtifact
    device_id: str
    id: str
    request_id: str
    def __init__(self, id: _Optional[str] = ..., request_id: _Optional[str] = ..., device_id: _Optional[str] = ..., active_model_artifacts: _Optional[_Union[ModelArtifact, _Mapping]] = ...) -> None: ...

class DeviceDeployRequestMap(_message.Message):
    __slots__ = ["device_deploy_message_latest_response", "device_deploy_message_request"]
    DEVICE_DEPLOY_MESSAGE_LATEST_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_DEPLOY_MESSAGE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    device_deploy_message_latest_response: ModelMessageHistory
    device_deploy_message_request: ModelMessageHistory
    def __init__(self, device_deploy_message_request: _Optional[_Union[ModelMessageHistory, _Mapping]] = ..., device_deploy_message_latest_response: _Optional[_Union[ModelMessageHistory, _Mapping]] = ...) -> None: ...

class DeviceModelDeployRequest(_message.Message):
    __slots__ = ["configs", "deployment_request_id", "device_id", "id", "model"]
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    configs: VersionedConfigs
    deployment_request_id: str
    device_id: str
    id: str
    model: ModelArtifact
    def __init__(self, id: _Optional[str] = ..., deployment_request_id: _Optional[str] = ..., device_id: _Optional[str] = ..., model: _Optional[_Union[ModelArtifact, _Mapping]] = ..., configs: _Optional[_Union[VersionedConfigs, _Mapping]] = ...) -> None: ...

class DeviceModelDeployResponse(_message.Message):
    __slots__ = ["delivery_status", "device_id", "id", "request_id"]
    class DeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_COMPLETED: DeviceModelDeployResponse.DeliveryStatus
    DEPLOYMENT_FAILED: DeviceModelDeployResponse.DeliveryStatus
    DEPLOYMENT_INITIATED: DeviceModelDeployResponse.DeliveryStatus
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: DeviceModelDeployResponse.DeliveryStatus
    delivery_status: DeviceModelDeployResponse.DeliveryStatus
    device_id: str
    id: str
    request_id: str
    def __init__(self, id: _Optional[str] = ..., request_id: _Optional[str] = ..., device_id: _Optional[str] = ..., delivery_status: _Optional[_Union[DeviceModelDeployResponse.DeliveryStatus, str]] = ...) -> None: ...

class HistoricConfigsRequest(_message.Message):
    __slots__ = ["id", "num_of_configs"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NUM_OF_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    num_of_configs: int
    def __init__(self, id: _Optional[str] = ..., num_of_configs: _Optional[int] = ...) -> None: ...

class HistoricConfigsResponse(_message.Message):
    __slots__ = ["configs", "id"]
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[VersionedConfigs]
    id: str
    def __init__(self, id: _Optional[str] = ..., configs: _Optional[_Iterable[_Union[VersionedConfigs, _Mapping]]] = ...) -> None: ...

class HistoricDeviceDeployRequest(_message.Message):
    __slots__ = ["device", "id", "num_of_deploys"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NUM_OF_DEPLOYS_FIELD_NUMBER: _ClassVar[int]
    device: _graph_models_pb2.Device
    id: str
    num_of_deploys: int
    def __init__(self, id: _Optional[str] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ..., num_of_deploys: _Optional[int] = ...) -> None: ...

class HistoricDeviceDeployResponse(_message.Message):
    __slots__ = ["device_deploy_history", "id"]
    DEVICE_DEPLOY_HISTORY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    device_deploy_history: _containers.RepeatedCompositeFieldContainer[DeviceDeployRequestMap]
    id: str
    def __init__(self, id: _Optional[str] = ..., device_deploy_history: _Optional[_Iterable[_Union[DeviceDeployRequestMap, _Mapping]]] = ...) -> None: ...

class ModelArtifact(_message.Message):
    __slots__ = ["feature_extractor", "id", "object_detection", "tracker", "version"]
    FEATURE_EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_DETECTION_FIELD_NUMBER: _ClassVar[int]
    TRACKER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    feature_extractor: str
    id: str
    object_detection: str
    tracker: str
    version: str
    def __init__(self, id: _Optional[str] = ..., version: _Optional[str] = ..., object_detection: _Optional[str] = ..., feature_extractor: _Optional[str] = ..., tracker: _Optional[str] = ...) -> None: ...

class ModelMessageHistory(_message.Message):
    __slots__ = ["active_model_request", "active_model_response", "deploy_model_request", "device_model_deploy_request", "device_model_deploy_response", "id", "timestamp"]
    ACTIVE_MODEL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_MODEL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_MODEL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODEL_DEPLOY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODEL_DEPLOY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    active_model_request: DeviceActiveModelRequest
    active_model_response: DeviceActiveModelResponse
    deploy_model_request: DeployModelRequest
    device_model_deploy_request: DeviceModelDeployRequest
    device_model_deploy_response: DeviceModelDeployResponse
    id: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., device_model_deploy_request: _Optional[_Union[DeviceModelDeployRequest, _Mapping]] = ..., device_model_deploy_response: _Optional[_Union[DeviceModelDeployResponse, _Mapping]] = ..., active_model_request: _Optional[_Union[DeviceActiveModelRequest, _Mapping]] = ..., active_model_response: _Optional[_Union[DeviceActiveModelResponse, _Mapping]] = ..., deploy_model_request: _Optional[_Union[DeployModelRequest, _Mapping]] = ...) -> None: ...

class ResponseLatestArtifacts(_message.Message):
    __slots__ = ["configs", "id"]
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    configs: VersionedConfigs
    id: str
    def __init__(self, id: _Optional[str] = ..., configs: _Optional[_Union[VersionedConfigs, _Mapping]] = ...) -> None: ...

class VersionedConfigs(_message.Message):
    __slots__ = ["configs_json", "created", "id"]
    CONFIGS_JSON_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    configs_json: str
    created: _timestamp_pb2.Timestamp
    id: str
    def __init__(self, id: _Optional[str] = ..., configs_json: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
