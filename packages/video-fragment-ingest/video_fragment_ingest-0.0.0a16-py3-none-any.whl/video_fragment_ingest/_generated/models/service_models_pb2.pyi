from google.protobuf import timestamp_pb2 as _timestamp_pb2
from models import graph_models_pb2 as _graph_models_pb2
from models import ai_models_pb2 as _ai_models_pb2
from models import model_deployment_pb2 as _model_deployment_pb2
from models import spatial_models_pb2 as _spatial_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Authentication(_message.Message):
    __slots__ = ["access_token", "id_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    id_token: str
    def __init__(self, id_token: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class BadgeReaderWithRelationships(_message.Message):
    __slots__ = ["badge_reader", "campus_id", "level_id", "zone_id"]
    BADGE_READER_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    badge_reader: _graph_models_pb2.BadgeReader
    campus_id: str
    level_id: str
    zone_id: str
    def __init__(self, badge_reader: _Optional[_Union[_graph_models_pb2.BadgeReader, _Mapping]] = ..., zone_id: _Optional[str] = ..., level_id: _Optional[str] = ..., campus_id: _Optional[str] = ...) -> None: ...

class CameraIdentifier(_message.Message):
    __slots__ = ["cameraId", "customerId", "facilityId"]
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMERID_FIELD_NUMBER: _ClassVar[int]
    FACILITYID_FIELD_NUMBER: _ClassVar[int]
    cameraId: str
    customerId: str
    facilityId: str
    def __init__(self, cameraId: _Optional[str] = ..., facilityId: _Optional[str] = ..., customerId: _Optional[str] = ...) -> None: ...

class CameraIdentifierList(_message.Message):
    __slots__ = ["cameras"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[CameraIdentifier]
    def __init__(self, cameras: _Optional[_Iterable[_Union[CameraIdentifier, _Mapping]]] = ...) -> None: ...

class CameraWithRelationships(_message.Message):
    __slots__ = ["camera", "campus_id", "level_id", "zone_id"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    camera: _graph_models_pb2.Camera
    campus_id: str
    level_id: str
    zone_id: str
    def __init__(self, camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., zone_id: _Optional[str] = ..., level_id: _Optional[str] = ..., campus_id: _Optional[str] = ...) -> None: ...

class CamerasInFacility(_message.Message):
    __slots__ = ["badge_readers", "cameras", "campuses", "facility_objects", "levels", "zones"]
    BADGE_READERS_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CAMPUSES_FIELD_NUMBER: _ClassVar[int]
    FACILITY_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    badge_readers: _containers.RepeatedCompositeFieldContainer[BadgeReaderWithRelationships]
    cameras: _containers.RepeatedCompositeFieldContainer[CameraWithRelationships]
    campuses: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Campus]
    facility_objects: _containers.RepeatedCompositeFieldContainer[FacilityObjectWithRelationships]
    levels: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Level]
    zones: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Zone]
    def __init__(self, levels: _Optional[_Iterable[_Union[_graph_models_pb2.Level, _Mapping]]] = ..., zones: _Optional[_Iterable[_Union[_graph_models_pb2.Zone, _Mapping]]] = ..., campuses: _Optional[_Iterable[_Union[_graph_models_pb2.Campus, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[CameraWithRelationships, _Mapping]]] = ..., badge_readers: _Optional[_Iterable[_Union[BadgeReaderWithRelationships, _Mapping]]] = ..., facility_objects: _Optional[_Iterable[_Union[FacilityObjectWithRelationships, _Mapping]]] = ...) -> None: ...

class CloudStats(_message.Message):
    __slots__ = ["id", "runing_streams", "utilization"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RUNING_STREAMS_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    runing_streams: _containers.RepeatedCompositeFieldContainer[KVSStream]
    utilization: float
    def __init__(self, id: _Optional[str] = ..., utilization: _Optional[float] = ..., runing_streams: _Optional[_Iterable[_Union[KVSStream, _Mapping]]] = ...) -> None: ...

class CloudStreamTask(_message.Message):
    __slots__ = ["add_stream", "remove_stream"]
    ADD_STREAM_FIELD_NUMBER: _ClassVar[int]
    REMOVE_STREAM_FIELD_NUMBER: _ClassVar[int]
    add_stream: KVSStream
    remove_stream: KVSStream
    def __init__(self, add_stream: _Optional[_Union[KVSStream, _Mapping]] = ..., remove_stream: _Optional[_Union[KVSStream, _Mapping]] = ...) -> None: ...

class CloudVideoDecodingIdentifier(_message.Message):
    __slots__ = ["camera_id", "customer_id", "facility_id", "id", "start_time"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    customer_id: str
    facility_id: str
    id: str
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., customer_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CustomRuleEvent(_message.Message):
    __slots__ = ["camera_ids", "customer_id", "facility_id", "id", "rule_setting", "timestamp"]
    CAMERA_IDS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    camera_ids: _containers.RepeatedScalarFieldContainer[str]
    customer_id: str
    facility_id: str
    id: str
    rule_setting: _graph_models_pb2.RuleSetting
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., camera_ids: _Optional[_Iterable[str]] = ..., rule_setting: _Optional[_Union[_graph_models_pb2.RuleSetting, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EnvironmentChange(_message.Message):
    __slots__ = ["badgeReaderId", "cameraId", "evidences", "facilityId", "scope", "sensorId", "systemEventId", "timestamp", "zoneId"]
    class ScopeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BADGEREADERID_FIELD_NUMBER: _ClassVar[int]
    BADGE_READER: EnvironmentChange.ScopeType
    CAMERA: EnvironmentChange.ScopeType
    CAMERAID_FIELD_NUMBER: _ClassVar[int]
    EVIDENCES_FIELD_NUMBER: _ClassVar[int]
    FACILITY: EnvironmentChange.ScopeType
    FACILITYID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    SENSORID_FIELD_NUMBER: _ClassVar[int]
    SYSTEMEVENTID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: EnvironmentChange.ScopeType
    VAPE_DETECTOR: EnvironmentChange.ScopeType
    ZONE: EnvironmentChange.ScopeType
    ZONEID_FIELD_NUMBER: _ClassVar[int]
    badgeReaderId: str
    cameraId: str
    evidences: _containers.RepeatedScalarFieldContainer[str]
    facilityId: str
    scope: EnvironmentChange.ScopeType
    sensorId: str
    systemEventId: str
    timestamp: _timestamp_pb2.Timestamp
    zoneId: str
    def __init__(self, facilityId: _Optional[str] = ..., cameraId: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., zoneId: _Optional[str] = ..., scope: _Optional[_Union[EnvironmentChange.ScopeType, str]] = ..., evidences: _Optional[_Iterable[str]] = ..., badgeReaderId: _Optional[str] = ..., systemEventId: _Optional[str] = ..., sensorId: _Optional[str] = ...) -> None: ...

class FFProbRequest(_message.Message):
    __slots__ = ["cameras", "id"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Camera]
    id: str
    def __init__(self, id: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[_graph_models_pb2.Camera, _Mapping]]] = ...) -> None: ...

class FFProbResponse(_message.Message):
    __slots__ = ["camera_id", "error", "id", "online", "output", "request_id", "timestamp"]
    class ErrorEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class OutputEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    error: _containers.ScalarMap[str, str]
    id: str
    online: bool
    output: _containers.ScalarMap[str, str]
    request_id: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., request_id: _Optional[str] = ..., camera_id: _Optional[str] = ..., output: _Optional[_Mapping[str, str]] = ..., error: _Optional[_Mapping[str, str]] = ..., online: bool = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FacilityObjectWithRelationships(_message.Message):
    __slots__ = ["badge_reader", "campus_id", "level_id", "vape_detector", "zone_id"]
    BADGE_READER_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ID_FIELD_NUMBER: _ClassVar[int]
    VAPE_DETECTOR_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    badge_reader: _graph_models_pb2.BadgeReader
    campus_id: str
    level_id: str
    vape_detector: _graph_models_pb2.VapeDetector
    zone_id: str
    def __init__(self, zone_id: _Optional[str] = ..., level_id: _Optional[str] = ..., campus_id: _Optional[str] = ..., badge_reader: _Optional[_Union[_graph_models_pb2.BadgeReader, _Mapping]] = ..., vape_detector: _Optional[_Union[_graph_models_pb2.VapeDetector, _Mapping]] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ["device", "id", "timestamp"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    device: _graph_models_pb2.Device
    id: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ...) -> None: ...

class KVSStream(_message.Message):
    __slots__ = ["camera_id", "customer_id", "facility_id"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    customer_id: str
    facility_id: str
    def __init__(self, camera_id: _Optional[str] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ...) -> None: ...

class KvsVideoUploadRequest(_message.Message):
    __slots__ = ["camera_id", "id", "start_time", "stop_time"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STOP_TIME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    id: str
    start_time: _timestamp_pb2.Timestamp
    stop_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., stop_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ManifestRequest(_message.Message):
    __slots__ = ["camera_id"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    def __init__(self, camera_id: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["active_device_model_request", "active_device_model_response", "add_camera", "audio_request", "camera_heartbeat", "channel", "delete_camera", "description", "device_heartbeat", "device_model_deploy_request", "device_model_deploy_response", "event", "facility_control", "ffprobe_request", "ffprobe_response", "floor_plan_completed", "frame", "frame_with_object", "heartbeat", "incident", "kvs_video_upload", "match_prediction", "media_request", "media_response", "notification", "pair_camera_request", "pairing_mode", "rendering_frame", "restart_device", "restart_live_view", "start_kvs_stream", "start_live_view", "start_video_playback", "stop_kvs_stream", "sub_request", "system_event", "testing_request", "timestamp", "update_camera", "upload_manifest", "upload_thumbnail_request", "upload_video_segment", "web_rtc_heartbeat"]
    ACTIVE_DEVICE_MODEL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DEVICE_MODEL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ADD_CAMERA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CAMERA_HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DELETE_CAMERA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODEL_DEPLOY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODEL_DEPLOY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_CONTROL_FIELD_NUMBER: _ClassVar[int]
    FFPROBE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FFPROBE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FLOOR_PLAN_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    FRAME_WITH_OBJECT_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    KVS_VIDEO_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    MATCH_PREDICTION_FIELD_NUMBER: _ClassVar[int]
    MEDIA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEDIA_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    PAIRING_MODE_FIELD_NUMBER: _ClassVar[int]
    PAIR_CAMERA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    RENDERING_FRAME_FIELD_NUMBER: _ClassVar[int]
    RESTART_DEVICE_FIELD_NUMBER: _ClassVar[int]
    RESTART_LIVE_VIEW_FIELD_NUMBER: _ClassVar[int]
    START_KVS_STREAM_FIELD_NUMBER: _ClassVar[int]
    START_LIVE_VIEW_FIELD_NUMBER: _ClassVar[int]
    START_VIDEO_PLAYBACK_FIELD_NUMBER: _ClassVar[int]
    STOP_KVS_STREAM_FIELD_NUMBER: _ClassVar[int]
    SUB_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_EVENT_FIELD_NUMBER: _ClassVar[int]
    TESTING_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UPDATE_CAMERA_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_THUMBNAIL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_VIDEO_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    WEB_RTC_HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    active_device_model_request: _model_deployment_pb2.DeviceActiveModelRequest
    active_device_model_response: _model_deployment_pb2.DeviceActiveModelResponse
    add_camera: _graph_models_pb2.Camera
    audio_request: PlayAudioRequest
    camera_heartbeat: _graph_models_pb2.Camera
    channel: str
    delete_camera: _graph_models_pb2.Camera
    description: str
    device_heartbeat: _graph_models_pb2.Device
    device_model_deploy_request: _model_deployment_pb2.DeviceModelDeployRequest
    device_model_deploy_response: _model_deployment_pb2.DeviceModelDeployResponse
    event: _graph_models_pb2.IncidentEvent
    facility_control: _graph_models_pb2.FacilityControl
    ffprobe_request: FFProbRequest
    ffprobe_response: FFProbResponse
    floor_plan_completed: _graph_models_pb2.FloorPlan
    frame: _ai_models_pb2.InferenceFrame
    frame_with_object: _graph_models_pb2.Camera
    heartbeat: Heartbeat
    incident: _graph_models_pb2.Incident
    kvs_video_upload: KvsVideoUploadRequest
    match_prediction: _graph_models_pb2.MatchPrediction
    media_request: UploadMediaRequest
    media_response: UploadMediaResponse
    notification: WebNotification
    pair_camera_request: PairCameraRequest
    pairing_mode: bool
    rendering_frame: _spatial_models_pb2.RenderingFrame
    restart_device: _graph_models_pb2.Device
    restart_live_view: _graph_models_pb2.Camera
    start_kvs_stream: StartKvsStreamRequest
    start_live_view: _graph_models_pb2.Camera
    start_video_playback: StartVideoPlaybackRequest
    stop_kvs_stream: StopKvsStreamRequest
    sub_request: SubscribeRequest
    system_event: _graph_models_pb2.SystemEvent
    testing_request: TestingRequest
    timestamp: _timestamp_pb2.Timestamp
    update_camera: _graph_models_pb2.Camera
    upload_manifest: ManifestRequest
    upload_thumbnail_request: UploadThumbnailRequest
    upload_video_segment: VideoSegmentRequest
    web_rtc_heartbeat: WebRTCHeartbeatRequest
    def __init__(self, channel: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., media_request: _Optional[_Union[UploadMediaRequest, _Mapping]] = ..., add_camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., update_camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., delete_camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., device_heartbeat: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ..., camera_heartbeat: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., sub_request: _Optional[_Union[SubscribeRequest, _Mapping]] = ..., media_response: _Optional[_Union[UploadMediaResponse, _Mapping]] = ..., pair_camera_request: _Optional[_Union[PairCameraRequest, _Mapping]] = ..., pairing_mode: bool = ..., event: _Optional[_Union[_graph_models_pb2.IncidentEvent, _Mapping]] = ..., testing_request: _Optional[_Union[TestingRequest, _Mapping]] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ..., notification: _Optional[_Union[WebNotification, _Mapping]] = ..., audio_request: _Optional[_Union[PlayAudioRequest, _Mapping]] = ..., restart_live_view: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., floor_plan_completed: _Optional[_Union[_graph_models_pb2.FloorPlan, _Mapping]] = ..., start_kvs_stream: _Optional[_Union[StartKvsStreamRequest, _Mapping]] = ..., stop_kvs_stream: _Optional[_Union[StopKvsStreamRequest, _Mapping]] = ..., kvs_video_upload: _Optional[_Union[KvsVideoUploadRequest, _Mapping]] = ..., upload_thumbnail_request: _Optional[_Union[UploadThumbnailRequest, _Mapping]] = ..., ffprobe_request: _Optional[_Union[FFProbRequest, _Mapping]] = ..., ffprobe_response: _Optional[_Union[FFProbResponse, _Mapping]] = ..., frame_with_object: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., start_video_playback: _Optional[_Union[StartVideoPlaybackRequest, _Mapping]] = ..., web_rtc_heartbeat: _Optional[_Union[WebRTCHeartbeatRequest, _Mapping]] = ..., start_live_view: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., upload_manifest: _Optional[_Union[ManifestRequest, _Mapping]] = ..., upload_video_segment: _Optional[_Union[VideoSegmentRequest, _Mapping]] = ..., active_device_model_request: _Optional[_Union[_model_deployment_pb2.DeviceActiveModelRequest, _Mapping]] = ..., active_device_model_response: _Optional[_Union[_model_deployment_pb2.DeviceActiveModelResponse, _Mapping]] = ..., device_model_deploy_request: _Optional[_Union[_model_deployment_pb2.DeviceModelDeployRequest, _Mapping]] = ..., device_model_deploy_response: _Optional[_Union[_model_deployment_pb2.DeviceModelDeployResponse, _Mapping]] = ..., match_prediction: _Optional[_Union[_graph_models_pb2.MatchPrediction, _Mapping]] = ..., rendering_frame: _Optional[_Union[_spatial_models_pb2.RenderingFrame, _Mapping]] = ..., facility_control: _Optional[_Union[_graph_models_pb2.FacilityControl, _Mapping]] = ..., restart_device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ..., system_event: _Optional[_Union[_graph_models_pb2.SystemEvent, _Mapping]] = ...) -> None: ...

class PairCameraRequest(_message.Message):
    __slots__ = ["conf_camera", "pos_camera"]
    CONF_CAMERA_FIELD_NUMBER: _ClassVar[int]
    POS_CAMERA_FIELD_NUMBER: _ClassVar[int]
    conf_camera: _graph_models_pb2.Camera
    pos_camera: _graph_models_pb2.Camera
    def __init__(self, conf_camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., pos_camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ...) -> None: ...

class PairMultiLensCameraRequest(_message.Message):
    __slots__ = ["conf_camera", "pos_camera"]
    CONF_CAMERA_FIELD_NUMBER: _ClassVar[int]
    POS_CAMERA_FIELD_NUMBER: _ClassVar[int]
    conf_camera: _graph_models_pb2.MultiLensCamera
    pos_camera: _graph_models_pb2.MultiLensCamera
    def __init__(self, conf_camera: _Optional[_Union[_graph_models_pb2.MultiLensCamera, _Mapping]] = ..., pos_camera: _Optional[_Union[_graph_models_pb2.MultiLensCamera, _Mapping]] = ...) -> None: ...

class PlayAudioRequest(_message.Message):
    __slots__ = ["audio", "speaker"]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_FIELD_NUMBER: _ClassVar[int]
    audio: _graph_models_pb2.SpeechAudio
    speaker: _graph_models_pb2.Speaker
    def __init__(self, speaker: _Optional[_Union[_graph_models_pb2.Speaker, _Mapping]] = ..., audio: _Optional[_Union[_graph_models_pb2.SpeechAudio, _Mapping]] = ...) -> None: ...

class PresignedUrl(_message.Message):
    __slots__ = ["expires", "url"]
    EXPIRES_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    expires: _timestamp_pb2.Timestamp
    url: str
    def __init__(self, url: _Optional[str] = ..., expires: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RemoveCameraLocationRequest(_message.Message):
    __slots__ = ["camera", "campus", "location"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    camera: _graph_models_pb2.Camera
    campus: _graph_models_pb2.Campus
    location: _graph_models_pb2.Location
    def __init__(self, location: _Optional[_Union[_graph_models_pb2.Location, _Mapping]] = ..., camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., campus: _Optional[_Union[_graph_models_pb2.Campus, _Mapping]] = ...) -> None: ...

class StartKvsStreamRequest(_message.Message):
    __slots__ = ["camera_id", "frame"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    frame: _ai_models_pb2.InferenceFrame
    def __init__(self, camera_id: _Optional[str] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ...) -> None: ...

class StartVideoPlaybackRequest(_message.Message):
    __slots__ = ["camera_id", "codec", "start_time", "stream_name"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    codec: str
    start_time: _timestamp_pb2.Timestamp
    stream_name: str
    def __init__(self, camera_id: _Optional[str] = ..., stream_name: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., codec: _Optional[str] = ...) -> None: ...

class StopKvsStreamRequest(_message.Message):
    __slots__ = ["camera_id"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    def __init__(self, camera_id: _Optional[str] = ...) -> None: ...

class SubscribeRequest(_message.Message):
    __slots__ = ["channels"]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, channels: _Optional[_Iterable[str]] = ...) -> None: ...

class TestingRequest(_message.Message):
    __slots__ = ["camera_id", "frame_count", "testing_type"]
    class TestingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    GUN: TestingRequest.TestingType
    LONG_GUN: TestingRequest.TestingType
    MAN_DOWN: TestingRequest.TestingType
    PERSON: TestingRequest.TestingType
    TESTING_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: TestingRequest.TestingType
    camera_id: str
    frame_count: int
    testing_type: TestingRequest.TestingType
    def __init__(self, testing_type: _Optional[_Union[TestingRequest.TestingType, str]] = ..., camera_id: _Optional[str] = ..., frame_count: _Optional[int] = ...) -> None: ...

class TrailLog(_message.Message):
    __slots__ = ["action", "created", "customer", "details", "facility", "id", "resource_name", "user"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    action: str
    created: _timestamp_pb2.Timestamp
    customer: _graph_models_pb2.Customer
    details: str
    facility: _graph_models_pb2.Facility
    id: str
    resource_name: str
    user: _graph_models_pb2.User
    def __init__(self, id: _Optional[str] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., action: _Optional[str] = ..., resource_name: _Optional[str] = ..., details: _Optional[str] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TrailLogField(_message.Message):
    __slots__ = ["actions", "customer_id", "resources"]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[str]
    customer_id: str
    resources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, customer_id: _Optional[str] = ..., actions: _Optional[_Iterable[str]] = ..., resources: _Optional[_Iterable[str]] = ...) -> None: ...

class TrailLogFieldRequest(_message.Message):
    __slots__ = ["customer", "user"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    user: _graph_models_pb2.User
    def __init__(self, customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ...) -> None: ...

class TrailLogList(_message.Message):
    __slots__ = ["logs"]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[TrailLog]
    def __init__(self, logs: _Optional[_Iterable[_Union[TrailLog, _Mapping]]] = ...) -> None: ...

class TrailLogRequest(_message.Message):
    __slots__ = ["actions", "asc", "customer_id", "detail", "from_timestamp", "resources", "size", "start_index", "to_timestamp", "user_id"]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    ASC_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[str]
    asc: bool
    customer_id: str
    detail: str
    from_timestamp: _timestamp_pb2.Timestamp
    resources: _containers.RepeatedScalarFieldContainer[str]
    size: int
    start_index: int
    to_timestamp: _timestamp_pb2.Timestamp
    user_id: str
    def __init__(self, start_index: _Optional[int] = ..., size: _Optional[int] = ..., asc: bool = ..., customer_id: _Optional[str] = ..., actions: _Optional[_Iterable[str]] = ..., resources: _Optional[_Iterable[str]] = ..., detail: _Optional[str] = ..., user_id: _Optional[str] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TwilioChannel(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TwilioConversationMessage(_message.Message):
    __slots__ = ["contact_id", "content", "conversation_id", "incident_id", "sender"]
    CONTACT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    contact_id: str
    content: str
    conversation_id: str
    incident_id: str
    sender: str
    def __init__(self, incident_id: _Optional[str] = ..., conversation_id: _Optional[str] = ..., sender: _Optional[str] = ..., content: _Optional[str] = ..., contact_id: _Optional[str] = ...) -> None: ...

class TwilioMessage(_message.Message):
    __slots__ = ["content", "phone"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    content: str
    phone: str
    def __init__(self, phone: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class TwilioParticipant(_message.Message):
    __slots__ = ["conversation_id", "phone"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    phone: str
    def __init__(self, conversation_id: _Optional[str] = ..., phone: _Optional[str] = ...) -> None: ...

class TwilioToken(_message.Message):
    __slots__ = ["conversation_id", "jwt"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    jwt: str
    def __init__(self, conversation_id: _Optional[str] = ..., jwt: _Optional[str] = ...) -> None: ...

class UploadMediaRequest(_message.Message):
    __slots__ = ["bucket", "camera_id", "end_timestamp", "event_id", "frame_ids", "id", "key", "start_timestamp", "type"]
    class MediaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOTH: UploadMediaRequest.MediaType
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_IDS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE: UploadMediaRequest.MediaType
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: UploadMediaRequest.MediaType
    VIDEO: UploadMediaRequest.MediaType
    bucket: str
    camera_id: str
    end_timestamp: _timestamp_pb2.Timestamp
    event_id: str
    frame_ids: _containers.RepeatedScalarFieldContainer[str]
    id: str
    key: str
    start_timestamp: _timestamp_pb2.Timestamp
    type: UploadMediaRequest.MediaType
    def __init__(self, id: _Optional[str] = ..., event_id: _Optional[str] = ..., camera_id: _Optional[str] = ..., frame_ids: _Optional[_Iterable[str]] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., type: _Optional[_Union[UploadMediaRequest.MediaType, str]] = ..., start_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadMediaResponse(_message.Message):
    __slots__ = ["chunks", "event_id", "id", "request_time"]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    chunks: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.MediaChunk]
    event_id: str
    id: str
    request_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., event_id: _Optional[str] = ..., chunks: _Optional[_Iterable[_Union[_graph_models_pb2.MediaChunk, _Mapping]]] = ..., request_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadThumbnailRequest(_message.Message):
    __slots__ = ["camera_id", "elapse_time", "id"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ELAPSE_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    elapse_time: float
    id: str
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., elapse_time: _Optional[float] = ...) -> None: ...

class UserLogin(_message.Message):
    __slots__ = ["email", "password"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class VideoIngestFragment(_message.Message):
    __slots__ = ["camera_id", "customer_id", "duration", "facility_id", "s3_uri", "start_ts", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    S3_URI_FIELD_NUMBER: _ClassVar[int]
    START_TS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    customer_id: str
    duration: float
    facility_id: str
    s3_uri: str
    start_ts: _timestamp_pb2.Timestamp
    tags: _containers.ScalarMap[str, str]
    def __init__(self, customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., camera_id: _Optional[str] = ..., s3_uri: _Optional[str] = ..., duration: _Optional[float] = ..., start_ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class VideoPlayback(_message.Message):
    __slots__ = ["camera_id", "end_time", "start_time"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    end_time: _timestamp_pb2.Timestamp
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, camera_id: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class VideoSegmentRequest(_message.Message):
    __slots__ = ["camera_id", "manifest_timestamp", "segment_filename"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_FILENAME_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    manifest_timestamp: str
    segment_filename: str
    def __init__(self, camera_id: _Optional[str] = ..., manifest_timestamp: _Optional[str] = ..., segment_filename: _Optional[str] = ...) -> None: ...

class WebNotification(_message.Message):
    __slots__ = ["message", "title", "type"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ERROR: WebNotification.Type
    INFO: WebNotification.Type
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: WebNotification.Type
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: WebNotification.Type
    WARNING: WebNotification.Type
    message: str
    title: str
    type: WebNotification.Type
    def __init__(self, title: _Optional[str] = ..., message: _Optional[str] = ..., type: _Optional[_Union[WebNotification.Type, str]] = ...) -> None: ...

class WebRTCHeartbeatRequest(_message.Message):
    __slots__ = ["stream_name"]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    stream_name: str
    def __init__(self, stream_name: _Optional[str] = ...) -> None: ...
