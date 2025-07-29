from google.protobuf import timestamp_pb2 as _timestamp_pb2
from models import ai_models_pb2 as _ai_models_pb2
from models import spatial_models_pb2 as _spatial_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class APIKey(_message.Message):
    __slots__ = ["created", "id", "key", "name", "secret", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    key: str
    name: str
    secret: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., key: _Optional[str] = ..., secret: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AccessControlEvent(_message.Message):
    __slots__ = ["authorized_badge_holder", "badge_reader", "confirmation_result", "id", "result", "string_tags", "validated_by"]
    class BadgeReaderResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ConfirmationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTHORIZED_BADGE_HOLDER_FIELD_NUMBER: _ClassVar[int]
    AUTO_CONFIRMED: AccessControlEvent.ConfirmationResult
    BADGE_READER_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_RESULT_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED: AccessControlEvent.ConfirmationResult
    DENIED: AccessControlEvent.BadgeReaderResult
    GRANTED: AccessControlEvent.BadgeReaderResult
    ID_FIELD_NUMBER: _ClassVar[int]
    MISMATCHED: AccessControlEvent.ConfirmationResult
    PENDING: AccessControlEvent.ConfirmationResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: AccessControlEvent.BadgeReaderResult
    UNKNOWN_STATUS: AccessControlEvent.ConfirmationResult
    VALIDATED_BY_FIELD_NUMBER: _ClassVar[int]
    authorized_badge_holder: AuthorizedBadgeHolder
    badge_reader: BadgeReader
    confirmation_result: AccessControlEvent.ConfirmationResult
    id: str
    result: AccessControlEvent.BadgeReaderResult
    string_tags: _containers.ScalarMap[str, str]
    validated_by: User
    def __init__(self, id: _Optional[str] = ..., result: _Optional[_Union[AccessControlEvent.BadgeReaderResult, str]] = ..., authorized_badge_holder: _Optional[_Union[AuthorizedBadgeHolder, _Mapping]] = ..., badge_reader: _Optional[_Union[BadgeReader, _Mapping]] = ..., confirmation_result: _Optional[_Union[AccessControlEvent.ConfirmationResult, str]] = ..., validated_by: _Optional[_Union[User, _Mapping]] = ..., string_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ActivityLog(_message.Message):
    __slots__ = ["comments", "created", "description", "event_id", "id", "incident_id", "media", "message", "type", "updated", "user"]
    class ActivityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACTION: ActivityLog.ActivityType
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EVENT: ActivityLog.ActivityType
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RECEIVED: ActivityLog.ActivityType
    MESSAGE_SENT: ActivityLog.ActivityType
    SYSTEM_MESSAGE: ActivityLog.ActivityType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: ActivityLog.ActivityType
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    USER_SESSION: ActivityLog.ActivityType
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    created: _timestamp_pb2.Timestamp
    description: str
    event_id: str
    id: str
    incident_id: str
    media: _containers.RepeatedCompositeFieldContainer[MediaChunk]
    message: str
    type: ActivityLog.ActivityType
    updated: _timestamp_pb2.Timestamp
    user: User
    def __init__(self, id: _Optional[str] = ..., description: _Optional[str] = ..., type: _Optional[_Union[ActivityLog.ActivityType, str]] = ..., event_id: _Optional[str] = ..., message: _Optional[str] = ..., comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., incident_id: _Optional[str] = ..., media: _Optional[_Iterable[_Union[MediaChunk, _Mapping]]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AuthorizedBadgeHolder(_message.Message):
    __slots__ = ["badge_image_url", "created", "customer", "first_seen", "id", "last_confirmed_frame", "last_seen", "name", "string_tags", "updated", "vendor_id"]
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BADGE_IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FIRST_SEEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_CONFIRMED_FRAME_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    badge_image_url: str
    created: _timestamp_pb2.Timestamp
    customer: Customer
    first_seen: _timestamp_pb2.Timestamp
    id: str
    last_confirmed_frame: _ai_models_pb2.InferenceFrame
    last_seen: _timestamp_pb2.Timestamp
    name: str
    string_tags: _containers.ScalarMap[str, str]
    updated: _timestamp_pb2.Timestamp
    vendor_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., vendor_id: _Optional[str] = ..., badge_image_url: _Optional[str] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., first_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_confirmed_frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., string_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class BadgeReader(_message.Message):
    __slots__ = ["cameras", "created", "door", "id", "name", "position_x", "position_y", "rotation", "updated", "vendor_id", "vendor_name"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DOOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    VENDOR_NAME_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    door: Door
    id: str
    name: str
    position_x: float
    position_y: float
    rotation: float
    updated: _timestamp_pb2.Timestamp
    vendor_id: str
    vendor_name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., vendor_id: _Optional[str] = ..., vendor_name: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., rotation: _Optional[float] = ..., door: _Optional[_Union[Door, _Mapping]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Boundary(_message.Message):
    __slots__ = ["height", "id", "points"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    height: float
    id: str
    points: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, id: _Optional[str] = ..., points: _Optional[_Iterable[_Union[Point, _Mapping]]] = ..., height: _Optional[float] = ...) -> None: ...

class Camera(_message.Message):
    __slots__ = ["arn", "aspect", "continuous_video_upload", "controller", "created", "customer_id", "decomposer_regions", "device_id", "disabled", "elevation", "encoding", "facility_id", "focal_length_mm", "fov", "fps", "id", "inference_status", "ip", "kvs_stream_arn", "last_calibrated", "latitude", "longitude", "mac_address", "magicplan_uid", "masks", "model", "model_name", "multi_lens_camera_id", "name", "password", "pitch", "port", "position_x", "position_y", "range", "recording_status", "resolution_height", "resolution_width", "rotation", "rtsp_url", "sensor_height_mm", "sensor_width_mm", "spatial_calibration_data", "statistic", "status", "status_updated", "streaming_status", "subnet_mask", "test_mode", "type", "updated", "use_tcp", "username", "yaw"]
    class CameraType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Controller(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class TestMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ARN_FIELD_NUMBER: _ClassVar[int]
    ASPECT_FIELD_NUMBER: _ClassVar[int]
    CAMERA_TYPE_UNKNOWN: Camera.CameraType
    CEILING: Camera.CameraType
    CLOUD: Camera.Controller
    CONTINUOUS_VIDEO_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DECOMPOSER_REGIONS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    EDGE: Camera.Controller
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FISHEYE: Camera.CameraType
    FOCAL_LENGTH_MM_FIELD_NUMBER: _ClassVar[int]
    FOV_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    IDLE: Camera.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_STATUS_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    KVS_STREAM_ARN_FIELD_NUMBER: _ClassVar[int]
    LAST_CALIBRATED_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    MASKS_FIELD_NUMBER: _ClassVar[int]
    MEDICAL: Camera.TestMode
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS: Camera.CameraType
    MULTI_LENS_CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NONE: Camera.TestMode
    OFFLINE: Camera.Status
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    RECORDING_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_WIDTH_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    RTSP_URL_FIELD_NUMBER: _ClassVar[int]
    SENSOR_HEIGHT_MM_FIELD_NUMBER: _ClassVar[int]
    SENSOR_WIDTH_MM_FIELD_NUMBER: _ClassVar[int]
    SPATIAL_CALIBRATION_DATA_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_UNKNOWN: Camera.Status
    STATUS_UPDATED_FIELD_NUMBER: _ClassVar[int]
    STREAMING: Camera.Status
    STREAMING_STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBNET_MASK_FIELD_NUMBER: _ClassVar[int]
    TEST_MODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_SOURCE: Camera.Controller
    UNKNOWN_TEST_CASE: Camera.TestMode
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USE_TCP_FIELD_NUMBER: _ClassVar[int]
    WALL: Camera.CameraType
    WEAPON: Camera.TestMode
    YAW_FIELD_NUMBER: _ClassVar[int]
    arn: str
    aspect: float
    continuous_video_upload: bool
    controller: Camera.Controller
    created: _timestamp_pb2.Timestamp
    customer_id: str
    decomposer_regions: _containers.RepeatedCompositeFieldContainer[DecomposerRegion]
    device_id: str
    disabled: bool
    elevation: float
    encoding: str
    facility_id: str
    focal_length_mm: float
    fov: float
    fps: int
    id: str
    inference_status: Camera.Status
    ip: str
    kvs_stream_arn: str
    last_calibrated: _timestamp_pb2.Timestamp
    latitude: float
    longitude: float
    mac_address: str
    magicplan_uid: str
    masks: _containers.RepeatedCompositeFieldContainer[Mask]
    model: CameraModel
    model_name: str
    multi_lens_camera_id: str
    name: str
    password: str
    pitch: float
    port: str
    position_x: float
    position_y: float
    range: float
    recording_status: Camera.Status
    resolution_height: int
    resolution_width: int
    rotation: int
    rtsp_url: str
    sensor_height_mm: float
    sensor_width_mm: float
    spatial_calibration_data: _spatial_models_pb2.SpatialCalibrationData
    statistic: str
    status: Camera.Status
    status_updated: _timestamp_pb2.Timestamp
    streaming_status: Camera.Status
    subnet_mask: str
    test_mode: Camera.TestMode
    type: Camera.CameraType
    updated: _timestamp_pb2.Timestamp
    use_tcp: bool
    username: str
    yaw: float
    def __init__(self, id: _Optional[str] = ..., mac_address: _Optional[str] = ..., name: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., model_name: _Optional[str] = ..., fps: _Optional[int] = ..., resolution_height: _Optional[int] = ..., resolution_width: _Optional[int] = ..., encoding: _Optional[str] = ..., arn: _Optional[str] = ..., device_id: _Optional[str] = ..., rtsp_url: _Optional[str] = ..., status: _Optional[_Union[Camera.Status, str]] = ..., status_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., magicplan_uid: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., elevation: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch: _Optional[float] = ..., fov: _Optional[float] = ..., aspect: _Optional[float] = ..., range: _Optional[float] = ..., type: _Optional[_Union[Camera.CameraType, str]] = ..., facility_id: _Optional[str] = ..., inference_status: _Optional[_Union[Camera.Status, str]] = ..., streaming_status: _Optional[_Union[Camera.Status, str]] = ..., recording_status: _Optional[_Union[Camera.Status, str]] = ..., masks: _Optional[_Iterable[_Union[Mask, _Mapping]]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., multi_lens_camera_id: _Optional[str] = ..., rotation: _Optional[int] = ..., kvs_stream_arn: _Optional[str] = ..., statistic: _Optional[str] = ..., decomposer_regions: _Optional[_Iterable[_Union[DecomposerRegion, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., test_mode: _Optional[_Union[Camera.TestMode, str]] = ..., controller: _Optional[_Union[Camera.Controller, str]] = ..., subnet_mask: _Optional[str] = ..., use_tcp: bool = ..., focal_length_mm: _Optional[float] = ..., sensor_width_mm: _Optional[float] = ..., sensor_height_mm: _Optional[float] = ..., model: _Optional[_Union[CameraModel, _Mapping]] = ..., last_calibrated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., disabled: bool = ..., spatial_calibration_data: _Optional[_Union[_spatial_models_pb2.SpatialCalibrationData, _Mapping]] = ..., continuous_video_upload: bool = ..., customer_id: _Optional[str] = ...) -> None: ...

class CameraManufacturer(_message.Message):
    __slots__ = ["created", "id", "models", "name", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    models: _containers.RepeatedCompositeFieldContainer[CameraModel]
    name: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., models: _Optional[_Iterable[_Union[CameraModel, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CameraModel(_message.Message):
    __slots__ = ["created", "focal_length_mm", "has_dynamic_zoom", "id", "is_ptz", "lenses", "name", "rtsp_url_templates", "sensor_height_mm", "sensor_width_mm", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    FOCAL_LENGTH_MM_FIELD_NUMBER: _ClassVar[int]
    HAS_DYNAMIC_ZOOM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_PTZ_FIELD_NUMBER: _ClassVar[int]
    LENSES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RTSP_URL_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    SENSOR_HEIGHT_MM_FIELD_NUMBER: _ClassVar[int]
    SENSOR_WIDTH_MM_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    focal_length_mm: float
    has_dynamic_zoom: bool
    id: str
    is_ptz: bool
    lenses: int
    name: str
    rtsp_url_templates: str
    sensor_height_mm: float
    sensor_width_mm: float
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., lenses: _Optional[int] = ..., is_ptz: bool = ..., has_dynamic_zoom: bool = ..., rtsp_url_templates: _Optional[str] = ..., focal_length_mm: _Optional[float] = ..., sensor_width_mm: _Optional[float] = ..., sensor_height_mm: _Optional[float] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Campus(_message.Message):
    __slots__ = ["cameras", "coordinates", "created", "customer_id", "facilities", "id", "multi_lens_cameras", "name", "speakers", "updated", "zones"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS_CAMERAS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SPEAKERS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    coordinates: _containers.RepeatedCompositeFieldContainer[Coordinate]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    facilities: _containers.RepeatedCompositeFieldContainer[Facility]
    id: str
    multi_lens_cameras: _containers.RepeatedCompositeFieldContainer[MultiLensCamera]
    name: str
    speakers: _containers.RepeatedCompositeFieldContainer[Speaker]
    updated: _timestamp_pb2.Timestamp
    zones: _containers.RepeatedCompositeFieldContainer[Zone]
    def __init__(self, id: _Optional[str] = ..., customer_id: _Optional[str] = ..., name: _Optional[str] = ..., zones: _Optional[_Iterable[_Union[Zone, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., speakers: _Optional[_Iterable[_Union[Speaker, _Mapping]]] = ..., facilities: _Optional[_Iterable[_Union[Facility, _Mapping]]] = ..., coordinates: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ..., multi_lens_cameras: _Optional[_Iterable[_Union[MultiLensCamera, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["content", "created", "id", "replies", "updated", "user_id"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    content: str
    created: _timestamp_pb2.Timestamp
    id: str
    replies: _containers.RepeatedCompositeFieldContainer[Comment]
    updated: _timestamp_pb2.Timestamp
    user_id: str
    def __init__(self, id: _Optional[str] = ..., content: _Optional[str] = ..., user_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., replies: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Contact(_message.Message):
    __slots__ = ["contact_points", "created", "email", "first_name", "id", "img_url", "last_name", "phone", "position", "priority", "updated"]
    CONTACT_POINTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMG_URL_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    contact_points: _containers.RepeatedCompositeFieldContainer[ContactPoint]
    created: _timestamp_pb2.Timestamp
    email: str
    first_name: str
    id: str
    img_url: str
    last_name: str
    phone: str
    position: str
    priority: int
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., position: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., priority: _Optional[int] = ..., img_url: _Optional[str] = ..., contact_points: _Optional[_Iterable[_Union[ContactPoint, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ContactPoint(_message.Message):
    __slots__ = ["email", "id", "phone_number"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    phone_number: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., phone_number: _Optional[str] = ...) -> None: ...

class Conversation(_message.Message):
    __slots__ = ["contact_id", "conversation_id", "id", "incident_id", "phone", "user_id", "with_participants"]
    CONTACT_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    WITH_PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    contact_id: str
    conversation_id: str
    id: str
    incident_id: str
    phone: str
    user_id: str
    with_participants: bool
    def __init__(self, id: _Optional[str] = ..., incident_id: _Optional[str] = ..., conversation_id: _Optional[str] = ..., user_id: _Optional[str] = ..., contact_id: _Optional[str] = ..., phone: _Optional[str] = ..., with_participants: bool = ...) -> None: ...

class Coordinate(_message.Message):
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

class CustomRule(_message.Message):
    __slots__ = ["created", "id", "name", "periodicity", "prompt", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERIODICITY_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    name: str
    periodicity: int
    prompt: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., prompt: _Optional[str] = ..., periodicity: _Optional[int] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Customer(_message.Message):
    __slots__ = ["audios", "campuses", "created", "domain", "escalation_policy", "facilities", "id", "is_archived", "name", "roles", "shifts", "tokens", "updated", "user_groups", "users"]
    AUDIOS_FIELD_NUMBER: _ClassVar[int]
    CAMPUSES_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    USER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    audios: _containers.RepeatedCompositeFieldContainer[SpeechAudio]
    campuses: _containers.RepeatedCompositeFieldContainer[Campus]
    created: _timestamp_pb2.Timestamp
    domain: str
    escalation_policy: EscalationPolicy
    facilities: _containers.RepeatedCompositeFieldContainer[Facility]
    id: str
    is_archived: bool
    name: str
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    shifts: _containers.RepeatedCompositeFieldContainer[Shift]
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    updated: _timestamp_pb2.Timestamp
    user_groups: _containers.RepeatedCompositeFieldContainer[UserGroup]
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., facilities: _Optional[_Iterable[_Union[Facility, _Mapping]]] = ..., domain: _Optional[str] = ..., audios: _Optional[_Iterable[_Union[SpeechAudio, _Mapping]]] = ..., campuses: _Optional[_Iterable[_Union[Campus, _Mapping]]] = ..., is_archived: bool = ..., user_groups: _Optional[_Iterable[_Union[UserGroup, _Mapping]]] = ..., roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ..., escalation_policy: _Optional[_Union[EscalationPolicy, _Mapping]] = ..., shifts: _Optional[_Iterable[_Union[Shift, _Mapping]]] = ..., tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CustomerList(_message.Message):
    __slots__ = ["customers"]
    CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    customers: _containers.RepeatedCompositeFieldContainer[Customer]
    def __init__(self, customers: _Optional[_Iterable[_Union[Customer, _Mapping]]] = ...) -> None: ...

class Daily(_message.Message):
    __slots__ = ["frequency", "id"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    id: str
    def __init__(self, id: _Optional[str] = ..., frequency: _Optional[int] = ...) -> None: ...

class DecomposerRegion(_message.Message):
    __slots__ = ["h", "id", "w", "x", "y"]
    H_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    h: float
    id: str
    w: float
    x: float
    y: float
    def __init__(self, id: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., w: _Optional[float] = ..., h: _Optional[float] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["arn", "cameras", "capacity", "cluster_id", "created", "customer_id", "facility_id", "id", "name", "position_x", "position_y", "speakers", "status", "status_updated", "subnet_mask", "sw_version", "system_uuid", "type", "updated"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ARN_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NANO: Device.Type
    OFFLINE: Device.Status
    ONLINE: Device.Status
    PAIRING: Device.Status
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    SPEAKERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_UPDATED_FIELD_NUMBER: _ClassVar[int]
    SUBNET_MASK_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_UUID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Device.Status
    UNKNOWN_TYPE: Device.Type
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    UPDATING: Device.Status
    X86_A100: Device.Type
    XAVIER: Device.Type
    XAVIER_AGX: Device.Type
    XAVIER_NX: Device.Type
    arn: str
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    capacity: int
    cluster_id: str
    created: _timestamp_pb2.Timestamp
    customer_id: str
    facility_id: str
    id: str
    name: str
    position_x: float
    position_y: float
    speakers: _containers.RepeatedCompositeFieldContainer[Speaker]
    status: Device.Status
    status_updated: _timestamp_pb2.Timestamp
    subnet_mask: str
    sw_version: str
    system_uuid: str
    type: Device.Type
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., sw_version: _Optional[str] = ..., facility_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[Device.Type, str]] = ..., system_uuid: _Optional[str] = ..., arn: _Optional[str] = ..., status: _Optional[_Union[Device.Status, str]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., status_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., customer_id: _Optional[str] = ..., cluster_id: _Optional[str] = ..., speakers: _Optional[_Iterable[_Union[Speaker, _Mapping]]] = ..., subnet_mask: _Optional[str] = ..., capacity: _Optional[int] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DeviceCluster(_message.Message):
    __slots__ = ["created", "customer_id", "devices", "facility_id", "id", "name", "position_x", "position_y", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    facility_id: str
    id: str
    name: str
    position_x: float
    position_y: float
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DisableCameras(_message.Message):
    __slots__ = ["cameras", "created", "duration", "facility_snapshot", "id", "updated"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    duration: int
    facility_snapshot: str
    id: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., duration: _Optional[int] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., facility_snapshot: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DisableCamerasLog(_message.Message):
    __slots__ = ["cameras", "created", "duration", "end", "facility", "id", "updated", "user"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    duration: int
    end: _timestamp_pb2.Timestamp
    facility: Facility
    id: str
    updated: _timestamp_pb2.Timestamp
    user: User
    def __init__(self, id: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., facility: _Optional[_Union[Facility, _Mapping]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., duration: _Optional[int] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Door(_message.Message):
    __slots__ = ["closed", "depth", "direction", "facility_id", "height", "hinge_position_x", "hinge_position_y", "id", "label", "latch_position_x", "latch_position_y", "leads_to", "magicplan_uid", "twin_magicplan_uid", "type", "width"]
    class DoorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    GARAGE: Door.DoorType
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HINGED_DOOR: Door.DoorType
    HINGED_DOUBLE_DOOR: Door.DoorType
    HINGE_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    HINGE_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LATCH_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    LATCH_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    LEADS_TO_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    OPENING: Door.DoorType
    TWIN_MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Door.DoorType
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    closed: bool
    depth: float
    direction: int
    facility_id: str
    height: float
    hinge_position_x: float
    hinge_position_y: float
    id: str
    label: str
    latch_position_x: float
    latch_position_y: float
    leads_to: _containers.RepeatedCompositeFieldContainer[Location]
    magicplan_uid: str
    twin_magicplan_uid: str
    type: Door.DoorType
    width: float
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., twin_magicplan_uid: _Optional[str] = ..., leads_to: _Optional[_Iterable[_Union[Location, _Mapping]]] = ..., label: _Optional[str] = ..., hinge_position_x: _Optional[float] = ..., hinge_position_y: _Optional[float] = ..., latch_position_x: _Optional[float] = ..., latch_position_y: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., depth: _Optional[float] = ..., direction: _Optional[int] = ..., type: _Optional[_Union[Door.DoorType, str]] = ..., facility_id: _Optional[str] = ..., closed: bool = ...) -> None: ...

class EmergencyCallProgress(_message.Message):
    __slots__ = ["created", "id", "incident_id", "status", "user"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CALL_END: EmergencyCallProgress.Status
    CALL_PLACED: EmergencyCallProgress.Status
    CANCEL: EmergencyCallProgress.Status
    COMPLETE: EmergencyCallProgress.Status
    CONFIRM: EmergencyCallProgress.Status
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    INITIATE: EmergencyCallProgress.Status
    RETRY: EmergencyCallProgress.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT: EmergencyCallProgress.Status
    UNKNOWN: EmergencyCallProgress.Status
    USER_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    incident_id: str
    status: EmergencyCallProgress.Status
    user: User
    def __init__(self, id: _Optional[str] = ..., incident_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., status: _Optional[_Union[EmergencyCallProgress.Status, str]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EscalationPolicy(_message.Message):
    __slots__ = ["created", "customer", "id", "name", "steps", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    customer: Customer
    id: str
    name: str
    steps: _containers.RepeatedCompositeFieldContainer[EscalationStep]
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[EscalationStep, _Mapping]]] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EscalationStep(_message.Message):
    __slots__ = ["created", "delay", "id", "index", "shifts", "updated", "users"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    delay: int
    id: str
    index: int
    shifts: _containers.RepeatedCompositeFieldContainer[Shift]
    updated: _timestamp_pb2.Timestamp
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, id: _Optional[str] = ..., index: _Optional[int] = ..., shifts: _Optional[_Iterable[_Union[Shift, _Mapping]]] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., delay: _Optional[int] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ["camera_id", "confidence", "created", "evidences", "id", "incident_id", "rule", "timestamp", "type", "updated", "verification"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Verification(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ARMED_PERSON_DETECTED: Event.Type
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    EVIDENCES_FIELD_NUMBER: _ClassVar[int]
    FALSE_POSITIVE: Event.Verification
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_COUNT: Event.Type
    PERSON_DETECTED: Event.Type
    POSITIVE: Event.Verification
    RULE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_TYPE: Event.Type
    UNKNOWN_VERIFICATION: Event.Verification
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    confidence: float
    created: _timestamp_pb2.Timestamp
    evidences: _containers.RepeatedCompositeFieldContainer[MediaChunk]
    id: str
    incident_id: str
    rule: RuleSetting
    timestamp: _timestamp_pb2.Timestamp
    type: Event.Type
    updated: _timestamp_pb2.Timestamp
    verification: Event.Verification
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., type: _Optional[_Union[Event.Type, str]] = ..., verification: _Optional[_Union[Event.Verification, str]] = ..., confidence: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., evidences: _Optional[_Iterable[_Union[MediaChunk, _Mapping]]] = ..., rule: _Optional[_Union[RuleSetting, _Mapping]] = ..., incident_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Export(_message.Message):
    __slots__ = ["bucket", "id", "key", "url"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    id: str
    key: str
    url: str
    def __init__(self, id: _Optional[str] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class Facility(_message.Message):
    __slots__ = ["access_key", "cameras", "campus_id", "city", "contacts", "created", "customer_id", "devices", "disable_rules", "escalation_policy", "floor_plan", "id", "img_url", "latitude", "longitude", "multi_lens_cameras", "name", "region", "rule_settings", "secret_key", "show_campus", "state", "street", "time_zone", "updated", "work_hours", "zipcode"]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_ID_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_RULES_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    FLOOR_PLAN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMG_URL_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS_CAMERAS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    SHOW_CAMPUS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    ZIPCODE_FIELD_NUMBER: _ClassVar[int]
    access_key: str
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    campus_id: str
    city: str
    contacts: _containers.RepeatedCompositeFieldContainer[Contact]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    disable_rules: bool
    escalation_policy: EscalationPolicy
    floor_plan: FloorPlan
    id: str
    img_url: str
    latitude: float
    longitude: float
    multi_lens_cameras: _containers.RepeatedCompositeFieldContainer[MultiLensCamera]
    name: str
    region: str
    rule_settings: _containers.RepeatedCompositeFieldContainer[RuleSetting]
    secret_key: str
    show_campus: bool
    state: str
    street: str
    time_zone: str
    updated: _timestamp_pb2.Timestamp
    work_hours: _containers.RepeatedCompositeFieldContainer[WorkHours]
    zipcode: str
    def __init__(self, customer_id: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zipcode: _Optional[str] = ..., longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., contacts: _Optional[_Iterable[_Union[Contact, _Mapping]]] = ..., floor_plan: _Optional[_Union[FloorPlan, _Mapping]] = ..., devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ..., access_key: _Optional[str] = ..., secret_key: _Optional[str] = ..., img_url: _Optional[str] = ..., region: _Optional[str] = ..., time_zone: _Optional[str] = ..., campus_id: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., multi_lens_cameras: _Optional[_Iterable[_Union[MultiLensCamera, _Mapping]]] = ..., show_campus: bool = ..., rule_settings: _Optional[_Iterable[_Union[RuleSetting, _Mapping]]] = ..., work_hours: _Optional[_Iterable[_Union[WorkHours, _Mapping]]] = ..., disable_rules: bool = ..., escalation_policy: _Optional[_Union[EscalationPolicy, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FacilityControl(_message.Message):
    __slots__ = ["completed", "created", "disable_cameras", "enable_facility", "facility", "id", "updated"]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DISABLE_CAMERAS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FACILITY_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    completed: _timestamp_pb2.Timestamp
    created: _timestamp_pb2.Timestamp
    disable_cameras: DisableCameras
    enable_facility: bool
    facility: Facility
    id: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., facility: _Optional[_Union[Facility, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., disable_cameras: _Optional[_Union[DisableCameras, _Mapping]] = ..., enable_facility: bool = ...) -> None: ...

class FacilitySnapshot(_message.Message):
    __slots__ = ["created", "floor_plan", "id", "outdoor", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    FLOOR_PLAN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OUTDOOR_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    floor_plan: str
    id: str
    outdoor: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., floor_plan: _Optional[str] = ..., outdoor: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FloorPlan(_message.Message):
    __slots__ = ["facility_id", "id", "is_editing", "label", "levels", "magicplan_uid", "plan_id", "projects", "use_export"]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_EDITING_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    USE_EXPORT_FIELD_NUMBER: _ClassVar[int]
    facility_id: str
    id: str
    is_editing: bool
    label: str
    levels: _containers.RepeatedCompositeFieldContainer[Level]
    magicplan_uid: str
    plan_id: str
    projects: _containers.RepeatedCompositeFieldContainer[MagicPlanProject]
    use_export: bool
    def __init__(self, id: _Optional[str] = ..., facility_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., levels: _Optional[_Iterable[_Union[Level, _Mapping]]] = ..., projects: _Optional[_Iterable[_Union[MagicPlanProject, _Mapping]]] = ..., is_editing: bool = ..., use_export: bool = ...) -> None: ...

class Furniture(_message.Message):
    __slots__ = ["depth", "height", "id", "label", "magicplan_uid", "orientation", "position_x", "position_y", "rotation", "type", "width"]
    class FurnitureType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    AED: Furniture.FurnitureType
    BADGE_READER: Furniture.FurnitureType
    BED: Furniture.FurnitureType
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    EXIT: Furniture.FurnitureType
    EXTINGUISHER: Furniture.FurnitureType
    FIRE_PULL: Furniture.FurnitureType
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    PARTITION_WALL: Furniture.FurnitureType
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SOFA: Furniture.FurnitureType
    TABLE: Furniture.FurnitureType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Furniture.FurnitureType
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    depth: float
    height: float
    id: str
    label: str
    magicplan_uid: str
    orientation: int
    position_x: float
    position_y: float
    rotation: float
    type: Furniture.FurnitureType
    width: float
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., depth: _Optional[float] = ..., orientation: _Optional[int] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., type: _Optional[_Union[Furniture.FurnitureType, str]] = ..., rotation: _Optional[float] = ...) -> None: ...

class Incident(_message.Message):
    __slots__ = ["activity_logs", "assignees", "auto_911", "cameras", "confirmed_by", "created", "customer", "customer_id", "emergency_progress", "end_timestamp", "escalated", "events", "export", "facility", "facility_id", "floor_plan", "frames", "id", "incident_status", "location_id", "progress", "risk_score", "room", "rule_id", "rule_setting_id", "severity", "snapshot", "start_timestamp", "status", "title", "tracking_job", "trigger_camera_id", "trigger_rule", "trigger_rule_id", "type", "updated", "zone", "zone_type"]
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACTIVE: Incident.Status
    ACTIVITY_LOGS_FIELD_NUMBER: _ClassVar[int]
    AI_FALSE_POSITIVE: Incident.Status
    AI_VALIDATION: Incident.Status
    ARMED_PERSON: Incident.Type
    ASSIGNEES_FIELD_NUMBER: _ClassVar[int]
    AUTO_911_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CAR_LOITERING: Incident.Type
    CLOSED: Incident.Status
    CONFIRMED: Incident.Status
    CONFIRMED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ESCALATED_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_FAILED: Incident.Status
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FALSE_POSITIVE: Incident.Status
    FIGHTING: Incident.Type
    FLOOR_PLAN_FIELD_NUMBER: _ClassVar[int]
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    INTRUSION: Incident.Type
    IN_REVIEW: Incident.Status
    LEVEL_1: Incident.Severity
    LEVEL_2: Incident.Severity
    LEVEL_3: Incident.Severity
    LEVEL_4: Incident.Severity
    LEVEL_5: Incident.Severity
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    LOITERING: Incident.Type
    MEDICAL_EMERGENCY: Incident.Type
    OBJECT_LEFT_BEHIND: Incident.Type
    OCCUPANCY_LIMIT_REACHED: Incident.Type
    OPEN: Incident.Status
    POC_IN_REVIEW: Incident.Status
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED: Incident.Status
    RISK_SCORE_FIELD_NUMBER: _ClassVar[int]
    ROBBERY: Incident.Type
    ROOM_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTING_ID_FIELD_NUMBER: _ClassVar[int]
    SEALED: Incident.Status
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TRACKING: Incident.Type
    TRACKING_JOB_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_RULE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_RULE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_SEVERITY: Incident.Severity
    UNKNOWN_STATUS: Incident.Status
    UNKNOWN_TYPE: Incident.Type
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_DETECTION: Incident.Type
    ZONE_FIELD_NUMBER: _ClassVar[int]
    ZONE_TYPE_FIELD_NUMBER: _ClassVar[int]
    activity_logs: _containers.RepeatedCompositeFieldContainer[ActivityLog]
    assignees: _containers.RepeatedCompositeFieldContainer[IncidentAssignment]
    auto_911: bool
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    confirmed_by: str
    created: _timestamp_pb2.Timestamp
    customer: Customer
    customer_id: str
    emergency_progress: _containers.RepeatedCompositeFieldContainer[EmergencyCallProgress]
    end_timestamp: _timestamp_pb2.Timestamp
    escalated: _containers.RepeatedCompositeFieldContainer[Contact]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    export: Export
    facility: Facility
    facility_id: str
    floor_plan: str
    frames: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.InferenceFrame]
    id: str
    incident_status: str
    location_id: str
    progress: _containers.RepeatedCompositeFieldContainer[IncidentProgress]
    risk_score: float
    room: str
    rule_id: str
    rule_setting_id: str
    severity: Incident.Severity
    snapshot: FacilitySnapshot
    start_timestamp: _timestamp_pb2.Timestamp
    status: Incident.Status
    title: str
    tracking_job: ObjectOfInterestTrackingJob
    trigger_camera_id: str
    trigger_rule: str
    trigger_rule_id: str
    type: Incident.Type
    updated: _timestamp_pb2.Timestamp
    zone: Zone
    zone_type: int
    def __init__(self, id: _Optional[str] = ..., facility_id: _Optional[str] = ..., type: _Optional[_Union[Incident.Type, str]] = ..., risk_score: _Optional[float] = ..., severity: _Optional[_Union[Incident.Severity, str]] = ..., status: _Optional[_Union[Incident.Status, str]] = ..., start_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ..., activity_logs: _Optional[_Iterable[_Union[ActivityLog, _Mapping]]] = ..., customer_id: _Optional[str] = ..., floor_plan: _Optional[str] = ..., rule_id: _Optional[str] = ..., title: _Optional[str] = ..., frames: _Optional[_Iterable[_Union[_ai_models_pb2.InferenceFrame, _Mapping]]] = ..., zone_type: _Optional[int] = ..., room: _Optional[str] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., facility: _Optional[_Union[Facility, _Mapping]] = ..., zone: _Optional[_Union[Zone, _Mapping]] = ..., trigger_camera_id: _Optional[str] = ..., confirmed_by: _Optional[str] = ..., escalated: _Optional[_Iterable[_Union[Contact, _Mapping]]] = ..., rule_setting_id: _Optional[str] = ..., progress: _Optional[_Iterable[_Union[IncidentProgress, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., trigger_rule_id: _Optional[str] = ..., export: _Optional[_Union[Export, _Mapping]] = ..., snapshot: _Optional[_Union[FacilitySnapshot, _Mapping]] = ..., auto_911: bool = ..., emergency_progress: _Optional[_Iterable[_Union[EmergencyCallProgress, _Mapping]]] = ..., location_id: _Optional[str] = ..., assignees: _Optional[_Iterable[_Union[IncidentAssignment, _Mapping]]] = ..., trigger_rule: _Optional[str] = ..., tracking_job: _Optional[_Union[ObjectOfInterestTrackingJob, _Mapping]] = ..., incident_status: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentAssignment(_message.Message):
    __slots__ = ["assignee", "created", "id", "receipt", "updated"]
    ASSIGNEE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    assignee: User
    created: _timestamp_pb2.Timestamp
    id: str
    receipt: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., assignee: _Optional[_Union[User, _Mapping]] = ..., receipt: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentEvent(_message.Message):
    __slots__ = ["comments", "created", "customer_id", "frame", "id", "incident_id", "log", "media", "timestamp", "tracking_record", "updated"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRACKING_RECORD_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    frame: _ai_models_pb2.InferenceFrame
    id: str
    incident_id: str
    log: ActivityLog
    media: MediaChunk
    timestamp: _timestamp_pb2.Timestamp
    tracking_record: ObjectTrackingRecord
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., incident_id: _Optional[str] = ..., comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., customer_id: _Optional[str] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., log: _Optional[_Union[ActivityLog, _Mapping]] = ..., media: _Optional[_Union[MediaChunk, _Mapping]] = ..., tracking_record: _Optional[_Union[ObjectTrackingRecord, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentEventList(_message.Message):
    __slots__ = ["events"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[IncidentEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[IncidentEvent, _Mapping]]] = ...) -> None: ...

class IncidentList(_message.Message):
    __slots__ = ["incidents"]
    INCIDENTS_FIELD_NUMBER: _ClassVar[int]
    incidents: _containers.RepeatedCompositeFieldContainer[Incident]
    def __init__(self, incidents: _Optional[_Iterable[_Union[Incident, _Mapping]]] = ...) -> None: ...

class IncidentProgress(_message.Message):
    __slots__ = ["created", "id", "status"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    status: Incident.Status
    def __init__(self, status: _Optional[_Union[Incident.Status, str]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class IncidentTrigger(_message.Message):
    __slots__ = ["camera", "frame", "id", "rule", "timestamp"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    camera: Camera
    frame: _ai_models_pb2.InferenceFrame
    id: str
    rule: RuleSetting
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, rule: _Optional[_Union[RuleSetting, _Mapping]] = ..., camera: _Optional[_Union[Camera, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ...) -> None: ...

class IncidentViewerSession(_message.Message):
    __slots__ = ["expiration", "id", "incident", "incident_id", "viewer_identity"]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    VIEWER_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    expiration: _timestamp_pb2.Timestamp
    id: str
    incident: Incident
    incident_id: str
    viewer_identity: str
    def __init__(self, id: _Optional[str] = ..., incident_id: _Optional[str] = ..., expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., incident: _Optional[_Union[Incident, _Mapping]] = ..., viewer_identity: _Optional[str] = ...) -> None: ...

class InferenceFrameList(_message.Message):
    __slots__ = ["frames"]
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    frames: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.InferenceFrame]
    def __init__(self, frames: _Optional[_Iterable[_Union[_ai_models_pb2.InferenceFrame, _Mapping]]] = ...) -> None: ...

class Level(_message.Message):
    __slots__ = ["floor_level", "id", "label", "locations", "magicplan_uid", "relative_x", "relative_y", "rotation", "walls", "zones"]
    FLOOR_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_X_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    WALLS_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    floor_level: int
    id: str
    label: str
    locations: _containers.RepeatedCompositeFieldContainer[Location]
    magicplan_uid: str
    relative_x: float
    relative_y: float
    rotation: float
    walls: _containers.RepeatedCompositeFieldContainer[Wall]
    zones: _containers.RepeatedCompositeFieldContainer[Zone]
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., floor_level: _Optional[int] = ..., locations: _Optional[_Iterable[_Union[Location, _Mapping]]] = ..., walls: _Optional[_Iterable[_Union[Wall, _Mapping]]] = ..., zones: _Optional[_Iterable[_Union[Zone, _Mapping]]] = ..., relative_x: _Optional[float] = ..., relative_y: _Optional[float] = ..., rotation: _Optional[float] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ["badge_readers", "boundary", "cameras", "device_clusters", "devices", "doors", "facility_id", "furniture", "id", "label", "magicplan_uid", "multi_lens_cameras", "speakers", "stairs", "type", "vape_detectors", "windows"]
    class LocationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BADGE_READERS_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    DOORS_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FURNITURE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LANDSCAPE: Location.LocationType
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS_CAMERAS_FIELD_NUMBER: _ClassVar[int]
    SPEAKERS_FIELD_NUMBER: _ClassVar[int]
    STAIRS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Location.LocationType
    VAPE_DETECTORS_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_FIELD_NUMBER: _ClassVar[int]
    badge_readers: _containers.RepeatedCompositeFieldContainer[BadgeReader]
    boundary: Boundary
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    device_clusters: _containers.RepeatedCompositeFieldContainer[DeviceCluster]
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    doors: _containers.RepeatedCompositeFieldContainer[Door]
    facility_id: str
    furniture: _containers.RepeatedCompositeFieldContainer[Furniture]
    id: str
    label: str
    magicplan_uid: str
    multi_lens_cameras: _containers.RepeatedCompositeFieldContainer[MultiLensCamera]
    speakers: _containers.RepeatedCompositeFieldContainer[Speaker]
    stairs: _containers.RepeatedCompositeFieldContainer[Stair]
    type: Location.LocationType
    vape_detectors: _containers.RepeatedCompositeFieldContainer[VapeDetector]
    windows: _containers.RepeatedCompositeFieldContainer[Window]
    def __init__(self, id: _Optional[str] = ..., facility_id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., boundary: _Optional[_Union[Boundary, _Mapping]] = ..., windows: _Optional[_Iterable[_Union[Window, _Mapping]]] = ..., doors: _Optional[_Iterable[_Union[Door, _Mapping]]] = ..., furniture: _Optional[_Iterable[_Union[Furniture, _Mapping]]] = ..., stairs: _Optional[_Iterable[_Union[Stair, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ..., device_clusters: _Optional[_Iterable[_Union[DeviceCluster, _Mapping]]] = ..., type: _Optional[_Union[Location.LocationType, str]] = ..., speakers: _Optional[_Iterable[_Union[Speaker, _Mapping]]] = ..., multi_lens_cameras: _Optional[_Iterable[_Union[MultiLensCamera, _Mapping]]] = ..., badge_readers: _Optional[_Iterable[_Union[BadgeReader, _Mapping]]] = ..., vape_detectors: _Optional[_Iterable[_Union[VapeDetector, _Mapping]]] = ...) -> None: ...

class MagicFloorPlan(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class MagicFloorPlans(_message.Message):
    __slots__ = ["magic_plans"]
    MAGIC_PLANS_FIELD_NUMBER: _ClassVar[int]
    magic_plans: _containers.RepeatedCompositeFieldContainer[MagicFloorPlan]
    def __init__(self, magic_plans: _Optional[_Iterable[_Union[MagicFloorPlan, _Mapping]]] = ...) -> None: ...

class MagicPlanProject(_message.Message):
    __slots__ = ["id", "plan_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    plan_id: str
    def __init__(self, id: _Optional[str] = ..., plan_id: _Optional[str] = ...) -> None: ...

class Mask(_message.Message):
    __slots__ = ["id", "points", "rules_by_mask", "type"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    EXCLUSION: Mask.Type
    ID_FIELD_NUMBER: _ClassVar[int]
    INCLUSION: Mask.Type
    POINTS_FIELD_NUMBER: _ClassVar[int]
    RULES_BY_MASK_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_TYPE: Mask.Type
    id: str
    points: _containers.RepeatedCompositeFieldContainer[NormalizedPoint]
    rules_by_mask: _containers.RepeatedCompositeFieldContainer[RuleSetting]
    type: Mask.Type
    def __init__(self, id: _Optional[str] = ..., points: _Optional[_Iterable[_Union[NormalizedPoint, _Mapping]]] = ..., type: _Optional[_Union[Mask.Type, str]] = ..., rules_by_mask: _Optional[_Iterable[_Union[RuleSetting, _Mapping]]] = ...) -> None: ...

class MatchPrediction(_message.Message):
    __slots__ = ["assignees", "confidence", "created", "decision_code", "distance", "id", "object_track_id_in_target_frame", "status", "target_frame", "time_diff", "tracked_object", "updated"]
    class MatchPredictionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ASSIGNEES_FIELD_NUMBER: _ClassVar[int]
    AUTO_CONFIRMED: MatchPrediction.MatchPredictionStatus
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED: MatchPrediction.MatchPredictionStatus
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DECISION_CODE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TRACK_ID_IN_TARGET_FRAME_FIELD_NUMBER: _ClassVar[int]
    REJECTED: MatchPrediction.MatchPredictionStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TARGET_FRAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT: MatchPrediction.MatchPredictionStatus
    TIME_DIFF_FIELD_NUMBER: _ClassVar[int]
    TRACKED_OBJECT_FIELD_NUMBER: _ClassVar[int]
    UNCONFIRMED: MatchPrediction.MatchPredictionStatus
    UNKNOWN: MatchPrediction.MatchPredictionStatus
    UNSURE: MatchPrediction.MatchPredictionStatus
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    assignees: _containers.RepeatedCompositeFieldContainer[MatchPredictionAssignment]
    confidence: float
    created: _timestamp_pb2.Timestamp
    decision_code: int
    distance: float
    id: str
    object_track_id_in_target_frame: str
    status: MatchPrediction.MatchPredictionStatus
    target_frame: _ai_models_pb2.InferenceFrame
    time_diff: float
    tracked_object: TrackedObject
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., object_track_id_in_target_frame: _Optional[str] = ..., target_frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., confidence: _Optional[float] = ..., status: _Optional[_Union[MatchPrediction.MatchPredictionStatus, str]] = ..., tracked_object: _Optional[_Union[TrackedObject, _Mapping]] = ..., assignees: _Optional[_Iterable[_Union[MatchPredictionAssignment, _Mapping]]] = ..., distance: _Optional[float] = ..., time_diff: _Optional[float] = ..., decision_code: _Optional[int] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MatchPredictionAssignment(_message.Message):
    __slots__ = ["assignee", "created", "id", "receipt", "updated"]
    ASSIGNEE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    assignee: User
    created: _timestamp_pb2.Timestamp
    id: str
    receipt: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., assignee: _Optional[_Union[User, _Mapping]] = ..., receipt: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MatchPredictionList(_message.Message):
    __slots__ = ["predictions"]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[MatchPrediction]
    def __init__(self, predictions: _Optional[_Iterable[_Union[MatchPrediction, _Mapping]]] = ...) -> None: ...

class MediaChunk(_message.Message):
    __slots__ = ["bucket", "camera_id", "created", "end_timestamp", "frame_id", "id", "key", "start_timestamp", "type", "updated", "url"]
    class MediaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FILE: MediaChunk.MediaType
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE: MediaChunk.MediaType
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: MediaChunk.MediaType
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    VIDEO: MediaChunk.MediaType
    bucket: str
    camera_id: str
    created: _timestamp_pb2.Timestamp
    end_timestamp: _timestamp_pb2.Timestamp
    frame_id: str
    id: str
    key: str
    start_timestamp: _timestamp_pb2.Timestamp
    type: MediaChunk.MediaType
    updated: _timestamp_pb2.Timestamp
    url: str
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., type: _Optional[_Union[MediaChunk.MediaType, str]] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., url: _Optional[str] = ..., frame_id: _Optional[str] = ..., start_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Monthly(_message.Message):
    __slots__ = ["day", "frequency", "id"]
    DAY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    day: int
    frequency: int
    id: str
    def __init__(self, id: _Optional[str] = ..., frequency: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...

class MultiLensCamera(_message.Message):
    __slots__ = ["aspect", "cameras", "created", "customer_id", "device_id", "elevation", "facility_id", "fov", "id", "name", "pitch", "position_x", "position_y", "range", "updated", "yaw"]
    ASPECT_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FOV_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    aspect: float
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    device_id: str
    elevation: float
    facility_id: str
    fov: float
    id: str
    name: str
    pitch: float
    position_x: float
    position_y: float
    range: float
    updated: _timestamp_pb2.Timestamp
    yaw: float
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., device_id: _Optional[str] = ..., elevation: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch: _Optional[float] = ..., fov: _Optional[float] = ..., aspect: _Optional[float] = ..., range: _Optional[float] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class NormalizedPoint(_message.Message):
    __slots__ = ["id", "index", "x", "y"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    id: str
    index: int
    x: float
    y: float
    def __init__(self, id: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., index: _Optional[int] = ...) -> None: ...

class ObjectOfInterestTrackingJob(_message.Message):
    __slots__ = ["created", "end", "id", "matches", "start", "status", "tracking_requests", "updated"]
    class ObjectOfInterestTrackingJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    COMPLETED: ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus
    CREATED_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS: ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT: ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus
    TRACKING_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    id: str
    matches: _containers.RepeatedCompositeFieldContainer[MatchPrediction]
    start: _timestamp_pb2.Timestamp
    status: ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus
    tracking_requests: _containers.RepeatedCompositeFieldContainer[ObjectsOfInterestRequest]
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[ObjectOfInterestTrackingJob.ObjectOfInterestTrackingJobStatus, str]] = ..., tracking_requests: _Optional[_Iterable[_Union[ObjectsOfInterestRequest, _Mapping]]] = ..., start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., matches: _Optional[_Iterable[_Union[MatchPrediction, _Mapping]]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ObjectTrackingRecord(_message.Message):
    __slots__ = ["description", "frame_id", "frame_url", "id", "object_of_interest"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_URL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    description: str
    frame_id: str
    frame_url: str
    id: str
    object_of_interest: _ai_models_pb2.DetectedObject
    def __init__(self, id: _Optional[str] = ..., frame_id: _Optional[str] = ..., frame_url: _Optional[str] = ..., description: _Optional[str] = ..., object_of_interest: _Optional[_Union[_ai_models_pb2.DetectedObject, _Mapping]] = ...) -> None: ...

class ObjectsOfInterestRequest(_message.Message):
    __slots__ = ["cancelled", "created", "id", "incident", "initiated_user", "object_of_interests", "timestamp", "updated"]
    CANCELLED_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INITIATED_USER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_OF_INTERESTS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    cancelled: bool
    created: _timestamp_pb2.Timestamp
    id: str
    incident: Incident
    initiated_user: User
    object_of_interests: _containers.RepeatedCompositeFieldContainer[TrackedObject]
    timestamp: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., incident: _Optional[_Union[Incident, _Mapping]] = ..., object_of_interests: _Optional[_Iterable[_Union[TrackedObject, _Mapping]]] = ..., initiated_user: _Optional[_Union[User, _Mapping]] = ..., cancelled: bool = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Permission(_message.Message):
    __slots__ = ["category", "created", "description", "id", "name", "updated"]
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_MANAGEMENT: Permission.Category
    ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_MANAGEMENT: Permission.Category
    NAME_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Permission.Category
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USER_MANAGEMENT: Permission.Category
    category: Permission.Category
    created: _timestamp_pb2.Timestamp
    description: str
    id: str
    name: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., category: _Optional[_Union[Permission.Category, str]] = ..., description: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ["id", "index", "magicplan_uid", "x", "y", "z"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    id: str
    index: int
    magicplan_uid: str
    x: float
    y: float
    z: float
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., index: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ["created", "customer_id", "description", "id", "name", "permissions", "protected", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    description: str
    id: str
    name: str
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    protected: bool
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ..., customer_id: _Optional[str] = ..., protected: bool = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RuleSetting(_message.Message):
    __slots__ = ["audio", "custom_rule", "description", "enable", "end_time", "escalation_policy", "friday", "id", "max_count", "min_count", "min_duration", "monday", "rapid_sos", "rule_id", "saturday", "start_time", "sunday", "thursday", "tuesday", "wednesday"]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_RULE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    FRIDAY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    MIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MIN_DURATION_FIELD_NUMBER: _ClassVar[int]
    MONDAY_FIELD_NUMBER: _ClassVar[int]
    RAPID_SOS_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    SATURDAY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    SUNDAY_FIELD_NUMBER: _ClassVar[int]
    THURSDAY_FIELD_NUMBER: _ClassVar[int]
    TUESDAY_FIELD_NUMBER: _ClassVar[int]
    WEDNESDAY_FIELD_NUMBER: _ClassVar[int]
    audio: SpeechAudio
    custom_rule: CustomRule
    description: str
    enable: bool
    end_time: int
    escalation_policy: EscalationPolicy
    friday: bool
    id: str
    max_count: int
    min_count: int
    min_duration: int
    monday: bool
    rapid_sos: bool
    rule_id: str
    saturday: bool
    start_time: int
    sunday: bool
    thursday: bool
    tuesday: bool
    wednesday: bool
    def __init__(self, id: _Optional[str] = ..., rule_id: _Optional[str] = ..., enable: bool = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., min_count: _Optional[int] = ..., max_count: _Optional[int] = ..., description: _Optional[str] = ..., monday: bool = ..., tuesday: bool = ..., wednesday: bool = ..., thursday: bool = ..., friday: bool = ..., saturday: bool = ..., sunday: bool = ..., audio: _Optional[_Union[SpeechAudio, _Mapping]] = ..., rapid_sos: bool = ..., min_duration: _Optional[int] = ..., escalation_policy: _Optional[_Union[EscalationPolicy, _Mapping]] = ..., custom_rule: _Optional[_Union[CustomRule, _Mapping]] = ...) -> None: ...

class Shift(_message.Message):
    __slots__ = ["created", "id", "name", "updated", "work_hours"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    name: str
    updated: _timestamp_pb2.Timestamp
    work_hours: _containers.RepeatedCompositeFieldContainer[WorkHours]
    def __init__(self, id: _Optional[str] = ..., work_hours: _Optional[_Iterable[_Union[WorkHours, _Mapping]]] = ..., name: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Speaker(_message.Message):
    __slots__ = ["created", "device_id", "elevation", "facility_id", "id", "ip", "mac_address", "magicplan_uid", "model_name", "name", "password", "pitch", "port", "position_x", "position_y", "sip_address", "updated", "username", "volume_level", "yaw"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    SIP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_LEVEL_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    device_id: str
    elevation: float
    facility_id: str
    id: str
    ip: str
    mac_address: str
    magicplan_uid: str
    model_name: str
    name: str
    password: str
    pitch: float
    port: str
    position_x: float
    position_y: float
    sip_address: str
    updated: _timestamp_pb2.Timestamp
    username: str
    volume_level: int
    yaw: float
    def __init__(self, id: _Optional[str] = ..., mac_address: _Optional[str] = ..., name: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., model_name: _Optional[str] = ..., volume_level: _Optional[int] = ..., sip_address: _Optional[str] = ..., device_id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., elevation: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch: _Optional[float] = ..., facility_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SpeechAudio(_message.Message):
    __slots__ = ["bucket", "created", "customer_id", "id", "key", "message", "updated", "url"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    created: _timestamp_pb2.Timestamp
    customer_id: str
    id: str
    key: str
    message: str
    updated: _timestamp_pb2.Timestamp
    url: str
    def __init__(self, id: _Optional[str] = ..., customer_id: _Optional[str] = ..., message: _Optional[str] = ..., key: _Optional[str] = ..., bucket: _Optional[str] = ..., url: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Stair(_message.Message):
    __slots__ = ["bottom", "depth", "height", "id", "label", "magicplan_uid", "position_x", "position_y", "steps", "top", "type", "width"]
    class StairType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CORNER_LANDING: Stair.StairType
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    L_SHAPED_LEFT: Stair.StairType
    L_SHAPED_RIGHT: Stair.StairType
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    ROUND_U_SHAPED: Stair.StairType
    STAIRCASE: Stair.StairType
    STEPS_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Stair.StairType
    U_SHAPED: Stair.StairType
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    bottom: float
    depth: float
    height: float
    id: str
    label: str
    magicplan_uid: str
    position_x: float
    position_y: float
    steps: int
    top: float
    type: Stair.StairType
    width: float
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., steps: _Optional[int] = ..., top: _Optional[float] = ..., bottom: _Optional[float] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., depth: _Optional[float] = ..., type: _Optional[_Union[Stair.StairType, str]] = ...) -> None: ...

class SystemEvent(_message.Message):
    __slots__ = ["access_control_event", "assignees", "cameras", "created", "customer", "description", "facility", "frames", "id", "location", "string_tags", "timestamp", "updated", "vape_detection_event", "zone"]
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ACCESS_CONTROL_EVENT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNEES_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VAPE_DETECTION_EVENT_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    access_control_event: AccessControlEvent
    assignees: _containers.RepeatedCompositeFieldContainer[UserAssignment]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    customer: Customer
    description: str
    facility: Facility
    frames: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.InferenceFrame]
    id: str
    location: Location
    string_tags: _containers.ScalarMap[str, str]
    timestamp: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    vape_detection_event: VapeDetectionEvent
    zone: Zone
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., facility: _Optional[_Union[Facility, _Mapping]] = ..., zone: _Optional[_Union[Zone, _Mapping]] = ..., location: _Optional[_Union[Location, _Mapping]] = ..., description: _Optional[str] = ..., assignees: _Optional[_Iterable[_Union[UserAssignment, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., frames: _Optional[_Iterable[_Union[_ai_models_pb2.InferenceFrame, _Mapping]]] = ..., access_control_event: _Optional[_Union[AccessControlEvent, _Mapping]] = ..., vape_detection_event: _Optional[_Union[VapeDetectionEvent, _Mapping]] = ..., string_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SystemEventList(_message.Message):
    __slots__ = ["events"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[SystemEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[SystemEvent, _Mapping]]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ["created", "created_by_user_id", "hash_algorithm", "hashed_token", "id", "last_used", "masked_token", "name", "permissions", "revoked", "revoked_at", "revoked_by_user_id", "updated"]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    HASHED_TOKEN_FIELD_NUMBER: _ClassVar[int]
    HASH_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_FIELD_NUMBER: _ClassVar[int]
    MASKED_TOKEN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    REVOKED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    REVOKED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    created_by_user_id: str
    hash_algorithm: str
    hashed_token: str
    id: str
    last_used: _timestamp_pb2.Timestamp
    masked_token: str
    name: str
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    revoked: bool
    revoked_at: _timestamp_pb2.Timestamp
    revoked_by_user_id: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., hashed_token: _Optional[str] = ..., masked_token: _Optional[str] = ..., hash_algorithm: _Optional[str] = ..., created_by_user_id: _Optional[str] = ..., permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ..., revoked: bool = ..., revoked_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., revoked_by_user_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_used: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TrackedObject(_message.Message):
    __slots__ = ["camera_id", "created", "customer_id", "detected_object", "facility_id", "frame_id", "global_id", "id", "timestamp", "tracking_job_id", "updated"]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    DETECTED_OBJECT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRACKING_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    created: _timestamp_pb2.Timestamp
    customer_id: str
    detected_object: _ai_models_pb2.DetectedObject
    facility_id: str
    frame_id: str
    global_id: str
    id: str
    timestamp: _timestamp_pb2.Timestamp
    tracking_job_id: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., global_id: _Optional[str] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., camera_id: _Optional[str] = ..., frame_id: _Optional[str] = ..., tracking_job_id: _Optional[str] = ..., detected_object: _Optional[_Union[_ai_models_pb2.DetectedObject, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TrackedObjectList(_message.Message):
    __slots__ = ["objects"]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[TrackedObject]
    def __init__(self, objects: _Optional[_Iterable[_Union[TrackedObject, _Mapping]]] = ...) -> None: ...

class UnConfirmedPredictionRequest(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["access_level", "auth", "availability", "birthdate", "created", "customer", "email", "first_name", "id", "last_name", "phone", "preferences", "priority", "profile", "profile_url", "provider_type", "role", "sessions", "status", "updated", "verified", "work_hours"]
    class AccessLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Availability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ProviderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class PreferencesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ACCESS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ADMIN: User.AccessLevel
    AUTH_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    AWAY: User.Status
    BIRTHDATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    EMAIL: User.ProviderType
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    GOOGLE: User.ProviderType
    IDLE: User.Availability
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER: User.AccessLevel
    OFFLINE: User.Availability
    OFF_DUTY: User.Status
    ONLINE: User.Availability
    ON_DUTY: User.Status
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_URL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SAML: User.ProviderType
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: User.AccessLevel
    UNKNOWN_AVAILABILITY: User.Availability
    UNKNOWN_PROVIDER_TYPE: User.ProviderType
    UNKNOWN_STATUS: User.Status
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    VOLT_OPERATOR: User.AccessLevel
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    access_level: User.AccessLevel
    auth: str
    availability: User.Availability
    birthdate: str
    created: _timestamp_pb2.Timestamp
    customer: Customer
    email: str
    first_name: str
    id: str
    last_name: str
    phone: str
    preferences: _containers.ScalarMap[str, str]
    priority: int
    profile: UserProfile
    profile_url: str
    provider_type: User.ProviderType
    role: str
    sessions: _containers.RepeatedCompositeFieldContainer[UserSession]
    status: User.Status
    updated: _timestamp_pb2.Timestamp
    verified: bool
    work_hours: _containers.RepeatedCompositeFieldContainer[WorkHours]
    def __init__(self, id: _Optional[str] = ..., auth: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., birthdate: _Optional[str] = ..., role: _Optional[str] = ..., profile_url: _Optional[str] = ..., access_level: _Optional[_Union[User.AccessLevel, str]] = ..., sessions: _Optional[_Iterable[_Union[UserSession, _Mapping]]] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., priority: _Optional[int] = ..., verified: bool = ..., profile: _Optional[_Union[UserProfile, _Mapping]] = ..., availability: _Optional[_Union[User.Availability, str]] = ..., status: _Optional[_Union[User.Status, str]] = ..., provider_type: _Optional[_Union[User.ProviderType, str]] = ..., work_hours: _Optional[_Iterable[_Union[WorkHours, _Mapping]]] = ..., preferences: _Optional[_Mapping[str, str]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserAssignment(_message.Message):
    __slots__ = ["assignee", "created", "id", "receipt", "updated"]
    ASSIGNEE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    assignee: User
    created: _timestamp_pb2.Timestamp
    id: str
    receipt: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., assignee: _Optional[_Union[User, _Mapping]] = ..., receipt: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserGroup(_message.Message):
    __slots__ = ["created", "customer_id", "facilities", "id", "name", "protected", "role", "updated", "users"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    customer_id: str
    facilities: _containers.RepeatedCompositeFieldContainer[Facility]
    id: str
    name: str
    protected: bool
    role: Role
    updated: _timestamp_pb2.Timestamp
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., facilities: _Optional[_Iterable[_Union[Facility, _Mapping]]] = ..., role: _Optional[_Union[Role, _Mapping]] = ..., customer_id: _Optional[str] = ..., protected: bool = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ["created", "id", "selected_customer_id", "selected_facility_id", "updated"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    selected_customer_id: str
    selected_facility_id: str
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., selected_customer_id: _Optional[str] = ..., selected_facility_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserSession(_message.Message):
    __slots__ = ["created", "id", "updated", "user_id"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    id: str
    updated: _timestamp_pb2.Timestamp
    user_id: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class VapeDetectionEvent(_message.Message):
    __slots__ = ["id", "string_tags", "vape_detector"]
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    VAPE_DETECTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    string_tags: _containers.ScalarMap[str, str]
    vape_detector: VapeDetector
    def __init__(self, id: _Optional[str] = ..., vape_detector: _Optional[_Union[VapeDetector, _Mapping]] = ..., string_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class VapeDetector(_message.Message):
    __slots__ = ["cameras", "created", "id", "manufacturer", "name", "position_x", "position_y", "rotation", "updated", "vendor_id", "vendor_name"]
    class Manufacturer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    HALO: VapeDetector.Manufacturer
    ID_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: VapeDetector.Manufacturer
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    VENDOR_NAME_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    created: _timestamp_pb2.Timestamp
    id: str
    manufacturer: VapeDetector.Manufacturer
    name: str
    position_x: float
    position_y: float
    rotation: float
    updated: _timestamp_pb2.Timestamp
    vendor_id: str
    vendor_name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., vendor_id: _Optional[str] = ..., vendor_name: _Optional[str] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., rotation: _Optional[float] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., manufacturer: _Optional[_Union[VapeDetector.Manufacturer, str]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class VideoFrame(_message.Message):
    __slots__ = ["bucket", "camera_id", "created", "id", "key", "timestamp", "updated"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    camera_id: str
    created: _timestamp_pb2.Timestamp
    id: str
    key: str
    timestamp: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ViolationTrigger(_message.Message):
    __slots__ = ["camera_id", "confidence", "facility_id", "frames", "id", "is_manual_trigger", "object_classes", "objects_of_interest", "risk_score", "rule", "rule_id", "severity", "system_event_id", "timestamp", "title", "triggered_by", "type", "zone"]
    class TriggeredBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FACILITY_WIDE_RULE: ViolationTrigger.TriggeredBy
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_MANUAL_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    LEVEL_WIDE_RULE: ViolationTrigger.TriggeredBy
    OBJECTS_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASSES_FIELD_NUMBER: _ClassVar[int]
    ON_DEMAND: ViolationTrigger.TriggeredBy
    RISK_SCORE_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_BY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: ViolationTrigger.TriggeredBy
    ZONE_FIELD_NUMBER: _ClassVar[int]
    ZONE_WIDE_RULE: ViolationTrigger.TriggeredBy
    camera_id: str
    confidence: float
    facility_id: str
    frames: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.InferenceFrame]
    id: str
    is_manual_trigger: bool
    object_classes: _containers.RepeatedScalarFieldContainer[_ai_models_pb2.DetectedObject.ObjectClass]
    objects_of_interest: _containers.RepeatedCompositeFieldContainer[_ai_models_pb2.DetectedObject]
    risk_score: float
    rule: RuleSetting
    rule_id: str
    severity: Incident.Severity
    system_event_id: str
    timestamp: _timestamp_pb2.Timestamp
    title: str
    triggered_by: ViolationTrigger.TriggeredBy
    type: Incident.Type
    zone: Zone
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[Incident.Type, str]] = ..., severity: _Optional[_Union[Incident.Severity, str]] = ..., facility_id: _Optional[str] = ..., camera_id: _Optional[str] = ..., confidence: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rule_id: _Optional[str] = ..., risk_score: _Optional[float] = ..., rule: _Optional[_Union[RuleSetting, _Mapping]] = ..., title: _Optional[str] = ..., zone: _Optional[_Union[Zone, _Mapping]] = ..., triggered_by: _Optional[_Union[ViolationTrigger.TriggeredBy, str]] = ..., is_manual_trigger: bool = ..., frames: _Optional[_Iterable[_Union[_ai_models_pb2.InferenceFrame, _Mapping]]] = ..., object_classes: _Optional[_Iterable[_Union[_ai_models_pb2.DetectedObject.ObjectClass, str]]] = ..., objects_of_interest: _Optional[_Iterable[_Union[_ai_models_pb2.DetectedObject, _Mapping]]] = ..., system_event_id: _Optional[str] = ...) -> None: ...

class Wall(_message.Message):
    __slots__ = ["height", "id", "thickness", "type", "x1", "x2", "y1", "y2"]
    class WallType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    EXTERIOR: Wall.WallType
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTERIOR: Wall.WallType
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Wall.WallType
    X1_FIELD_NUMBER: _ClassVar[int]
    X2_FIELD_NUMBER: _ClassVar[int]
    Y1_FIELD_NUMBER: _ClassVar[int]
    Y2_FIELD_NUMBER: _ClassVar[int]
    height: float
    id: str
    thickness: float
    type: Wall.WallType
    x1: float
    x2: float
    y1: float
    y2: float
    def __init__(self, id: _Optional[str] = ..., x1: _Optional[float] = ..., x2: _Optional[float] = ..., y1: _Optional[float] = ..., y2: _Optional[float] = ..., height: _Optional[float] = ..., thickness: _Optional[float] = ..., type: _Optional[_Union[Wall.WallType, str]] = ...) -> None: ...

class Weekly(_message.Message):
    __slots__ = ["frequency", "friday", "id", "monday", "saturday", "sunday", "thursday", "tuesday", "wednesday"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    FRIDAY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONDAY_FIELD_NUMBER: _ClassVar[int]
    SATURDAY_FIELD_NUMBER: _ClassVar[int]
    SUNDAY_FIELD_NUMBER: _ClassVar[int]
    THURSDAY_FIELD_NUMBER: _ClassVar[int]
    TUESDAY_FIELD_NUMBER: _ClassVar[int]
    WEDNESDAY_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    friday: bool
    id: str
    monday: bool
    saturday: bool
    sunday: bool
    thursday: bool
    tuesday: bool
    wednesday: bool
    def __init__(self, id: _Optional[str] = ..., frequency: _Optional[int] = ..., monday: bool = ..., tuesday: bool = ..., wednesday: bool = ..., thursday: bool = ..., friday: bool = ..., saturday: bool = ..., sunday: bool = ...) -> None: ...

class Window(_message.Message):
    __slots__ = ["depth", "distance_from_floor", "facility_id", "height", "id", "label", "left_position_x", "left_position_y", "magicplan_uid", "right_position_x", "right_position_y", "type", "width"]
    class WindowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    AWNING: Window.WindowType
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FROM_FLOOR_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    HUNG: Window.WindowType
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LEFT_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    LEFT_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    MAGICPLAN_UID_FIELD_NUMBER: _ClassVar[int]
    RIGHT_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    RIGHT_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    SLIDING: Window.WindowType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Window.WindowType
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    depth: float
    distance_from_floor: float
    facility_id: str
    height: float
    id: str
    label: str
    left_position_x: float
    left_position_y: float
    magicplan_uid: str
    right_position_x: float
    right_position_y: float
    type: Window.WindowType
    width: float
    def __init__(self, id: _Optional[str] = ..., magicplan_uid: _Optional[str] = ..., label: _Optional[str] = ..., left_position_x: _Optional[float] = ..., left_position_y: _Optional[float] = ..., right_position_x: _Optional[float] = ..., right_position_y: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., depth: _Optional[float] = ..., distance_from_floor: _Optional[float] = ..., type: _Optional[_Union[Window.WindowType, str]] = ..., facility_id: _Optional[str] = ...) -> None: ...

class WorkHours(_message.Message):
    __slots__ = ["created", "daily", "end_date", "end_time", "id", "monthly", "start_date", "start_time", "updated", "weekly"]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DAILY_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    WEEKLY_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    daily: Daily
    end_date: _timestamp_pb2.Timestamp
    end_time: int
    id: str
    monthly: Monthly
    start_date: _timestamp_pb2.Timestamp
    start_time: int
    updated: _timestamp_pb2.Timestamp
    weekly: Weekly
    def __init__(self, id: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., daily: _Optional[_Union[Daily, _Mapping]] = ..., weekly: _Optional[_Union[Weekly, _Mapping]] = ..., monthly: _Optional[_Union[Monthly, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Zone(_message.Message):
    __slots__ = ["badge_readers", "cameras", "coordinates", "escalation_policy", "id", "name", "rule_settings", "speakers", "type", "vape_detectors"]
    class ZoneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BADGE_READERS_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    HIGHLY_RESTRICTED: Zone.ZoneType
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLIC: Zone.ZoneType
    RESTRICTED: Zone.ZoneType
    RULE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SEMI_PUBLIC: Zone.ZoneType
    SPEAKERS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Zone.ZoneType
    VAPE_DETECTORS_FIELD_NUMBER: _ClassVar[int]
    badge_readers: _containers.RepeatedCompositeFieldContainer[BadgeReader]
    cameras: _containers.RepeatedCompositeFieldContainer[Camera]
    coordinates: _containers.RepeatedCompositeFieldContainer[Coordinate]
    escalation_policy: EscalationPolicy
    id: str
    name: str
    rule_settings: _containers.RepeatedCompositeFieldContainer[RuleSetting]
    speakers: _containers.RepeatedCompositeFieldContainer[Speaker]
    type: Zone.ZoneType
    vape_detectors: _containers.RepeatedCompositeFieldContainer[VapeDetector]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., coordinates: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ..., type: _Optional[_Union[Zone.ZoneType, str]] = ..., rule_settings: _Optional[_Iterable[_Union[RuleSetting, _Mapping]]] = ..., cameras: _Optional[_Iterable[_Union[Camera, _Mapping]]] = ..., speakers: _Optional[_Iterable[_Union[Speaker, _Mapping]]] = ..., escalation_policy: _Optional[_Union[EscalationPolicy, _Mapping]] = ..., badge_readers: _Optional[_Iterable[_Union[BadgeReader, _Mapping]]] = ..., vape_detectors: _Optional[_Iterable[_Union[VapeDetector, _Mapping]]] = ...) -> None: ...
