from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from models import ai_models_pb2 as _ai_models_pb2
from models import service_models_pb2 as _service_models_pb2
from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraDiagnosisRequest(_message.Message):
    __slots__ = ["cameras", "id"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Camera]
    id: str
    def __init__(self, id: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[_graph_models_pb2.Camera, _Mapping]]] = ...) -> None: ...

class CameraDiagnosisResultsRequest(_message.Message):
    __slots__ = ["cameras"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Camera]
    def __init__(self, cameras: _Optional[_Iterable[_Union[_graph_models_pb2.Camera, _Mapping]]] = ...) -> None: ...

class CameraDiagnosisResultsResponse(_message.Message):
    __slots__ = ["responses"]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[_service_models_pb2.FFProbResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[_service_models_pb2.FFProbResponse, _Mapping]]] = ...) -> None: ...

class CameraList(_message.Message):
    __slots__ = ["cameras"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Camera]
    def __init__(self, cameras: _Optional[_Iterable[_Union[_graph_models_pb2.Camera, _Mapping]]] = ...) -> None: ...

class CameraListRequest(_message.Message):
    __slots__ = ["customer", "facility"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    facility: _graph_models_pb2.Facility
    def __init__(self, customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ...) -> None: ...

class CameraMetadataResponse(_message.Message):
    __slots__ = ["customer", "facility"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    facility: _graph_models_pb2.Facility
    def __init__(self, customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ...) -> None: ...

class ClearFieldRequest(_message.Message):
    __slots__ = ["field", "graph_request"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    GRAPH_REQUEST_FIELD_NUMBER: _ClassVar[int]
    field: str
    graph_request: GraphRequest
    def __init__(self, graph_request: _Optional[_Union[GraphRequest, _Mapping]] = ..., field: _Optional[str] = ...) -> None: ...

class CustomIncidentRequest(_message.Message):
    __slots__ = ["facility", "frame", "image_data", "title", "user"]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    facility: _graph_models_pb2.Facility
    frame: _ai_models_pb2.InferenceFrame
    image_data: bytes
    title: str
    user: _graph_models_pb2.User
    def __init__(self, title: _Optional[str] = ..., frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., image_data: _Optional[bytes] = ...) -> None: ...

class DeviceList(_message.Message):
    __slots__ = ["devices"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[_graph_models_pb2.Device, _Mapping]]] = ...) -> None: ...

class EmergencyCallRequest(_message.Message):
    __slots__ = ["incident", "user"]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    incident: _graph_models_pb2.Incident
    user: _graph_models_pb2.User
    def __init__(self, incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ...) -> None: ...

class EventListRequest(_message.Message):
    __slots__ = ["asc", "from_timestamp", "incident_id", "size", "start_index", "to_timestamp"]
    ASC_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    asc: bool
    from_timestamp: _timestamp_pb2.Timestamp
    incident_id: str
    size: int
    start_index: int
    to_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, start_index: _Optional[int] = ..., size: _Optional[int] = ..., incident_id: _Optional[str] = ..., asc: bool = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FacilityControlList(_message.Message):
    __slots__ = ["controls"]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    controls: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.FacilityControl]
    def __init__(self, controls: _Optional[_Iterable[_Union[_graph_models_pb2.FacilityControl, _Mapping]]] = ...) -> None: ...

class FloorPlansRequest(_message.Message):
    __slots__ = ["plans"]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.FloorPlan]
    def __init__(self, plans: _Optional[_Iterable[_Union[_graph_models_pb2.FloorPlan, _Mapping]]] = ...) -> None: ...

class GraphRequest(_message.Message):
    __slots__ = ["activity_log", "api_key", "authorized_badge_holder", "badge_reader", "camera", "camera_manufacturer", "camera_model", "campus", "contact", "coordinate", "customer", "decomposer_region", "depth", "device", "device_cluster", "door", "event", "facility", "floor_plan", "furniture", "incident", "incident_event", "inference_frame", "kv_map", "level", "location", "mask", "multi_lens_camera", "object_of_interest_tracking_job", "permission", "role", "rule_setting", "shift", "speaker", "system_event", "user", "user_group", "user_session", "vape_detector", "wall", "work_hours", "zone"]
    class KvMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ACTIVITY_LOG_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_BADGE_HOLDER_FIELD_NUMBER: _ClassVar[int]
    BADGE_READER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MODEL_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    DECOMPOSER_REGION_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    DOOR_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FLOOR_PLAN_FIELD_NUMBER: _ClassVar[int]
    FURNITURE_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_EVENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    KV_MAP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS_CAMERA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_OF_INTEREST_TRACKING_JOB_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_EVENT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    USER_GROUP_FIELD_NUMBER: _ClassVar[int]
    USER_SESSION_FIELD_NUMBER: _ClassVar[int]
    VAPE_DETECTOR_FIELD_NUMBER: _ClassVar[int]
    WALL_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    activity_log: _graph_models_pb2.ActivityLog
    api_key: _graph_models_pb2.APIKey
    authorized_badge_holder: _graph_models_pb2.AuthorizedBadgeHolder
    badge_reader: _graph_models_pb2.BadgeReader
    camera: _graph_models_pb2.Camera
    camera_manufacturer: _graph_models_pb2.CameraManufacturer
    camera_model: _graph_models_pb2.CameraModel
    campus: _graph_models_pb2.Campus
    contact: _graph_models_pb2.Contact
    coordinate: _graph_models_pb2.Coordinate
    customer: _graph_models_pb2.Customer
    decomposer_region: _graph_models_pb2.DecomposerRegion
    depth: int
    device: _graph_models_pb2.Device
    device_cluster: _graph_models_pb2.DeviceCluster
    door: _graph_models_pb2.Door
    event: _graph_models_pb2.Event
    facility: _graph_models_pb2.Facility
    floor_plan: _graph_models_pb2.FloorPlan
    furniture: _graph_models_pb2.Furniture
    incident: _graph_models_pb2.Incident
    incident_event: _graph_models_pb2.IncidentEvent
    inference_frame: _ai_models_pb2.InferenceFrame
    kv_map: _containers.ScalarMap[str, str]
    level: _graph_models_pb2.Level
    location: _graph_models_pb2.Location
    mask: _graph_models_pb2.Mask
    multi_lens_camera: _graph_models_pb2.MultiLensCamera
    object_of_interest_tracking_job: _graph_models_pb2.ObjectOfInterestTrackingJob
    permission: _graph_models_pb2.Permission
    role: _graph_models_pb2.Role
    rule_setting: _graph_models_pb2.RuleSetting
    shift: _graph_models_pb2.Shift
    speaker: _graph_models_pb2.Speaker
    system_event: _graph_models_pb2.SystemEvent
    user: _graph_models_pb2.User
    user_group: _graph_models_pb2.UserGroup
    user_session: _graph_models_pb2.UserSession
    vape_detector: _graph_models_pb2.VapeDetector
    wall: _graph_models_pb2.Wall
    work_hours: _graph_models_pb2.WorkHours
    zone: _graph_models_pb2.Zone
    def __init__(self, user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ..., camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., contact: _Optional[_Union[_graph_models_pb2.Contact, _Mapping]] = ..., incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., api_key: _Optional[_Union[_graph_models_pb2.APIKey, _Mapping]] = ..., user_session: _Optional[_Union[_graph_models_pb2.UserSession, _Mapping]] = ..., level: _Optional[_Union[_graph_models_pb2.Level, _Mapping]] = ..., location: _Optional[_Union[_graph_models_pb2.Location, _Mapping]] = ..., floor_plan: _Optional[_Union[_graph_models_pb2.FloorPlan, _Mapping]] = ..., zone: _Optional[_Union[_graph_models_pb2.Zone, _Mapping]] = ..., event: _Optional[_Union[_graph_models_pb2.Event, _Mapping]] = ..., activity_log: _Optional[_Union[_graph_models_pb2.ActivityLog, _Mapping]] = ..., coordinate: _Optional[_Union[_graph_models_pb2.Coordinate, _Mapping]] = ..., device_cluster: _Optional[_Union[_graph_models_pb2.DeviceCluster, _Mapping]] = ..., rule_setting: _Optional[_Union[_graph_models_pb2.RuleSetting, _Mapping]] = ..., mask: _Optional[_Union[_graph_models_pb2.Mask, _Mapping]] = ..., campus: _Optional[_Union[_graph_models_pb2.Campus, _Mapping]] = ..., speaker: _Optional[_Union[_graph_models_pb2.Speaker, _Mapping]] = ..., multi_lens_camera: _Optional[_Union[_graph_models_pb2.MultiLensCamera, _Mapping]] = ..., furniture: _Optional[_Union[_graph_models_pb2.Furniture, _Mapping]] = ..., decomposer_region: _Optional[_Union[_graph_models_pb2.DecomposerRegion, _Mapping]] = ..., work_hours: _Optional[_Union[_graph_models_pb2.WorkHours, _Mapping]] = ..., permission: _Optional[_Union[_graph_models_pb2.Permission, _Mapping]] = ..., role: _Optional[_Union[_graph_models_pb2.Role, _Mapping]] = ..., user_group: _Optional[_Union[_graph_models_pb2.UserGroup, _Mapping]] = ..., shift: _Optional[_Union[_graph_models_pb2.Shift, _Mapping]] = ..., object_of_interest_tracking_job: _Optional[_Union[_graph_models_pb2.ObjectOfInterestTrackingJob, _Mapping]] = ..., inference_frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., camera_manufacturer: _Optional[_Union[_graph_models_pb2.CameraManufacturer, _Mapping]] = ..., camera_model: _Optional[_Union[_graph_models_pb2.CameraModel, _Mapping]] = ..., incident_event: _Optional[_Union[_graph_models_pb2.IncidentEvent, _Mapping]] = ..., badge_reader: _Optional[_Union[_graph_models_pb2.BadgeReader, _Mapping]] = ..., system_event: _Optional[_Union[_graph_models_pb2.SystemEvent, _Mapping]] = ..., authorized_badge_holder: _Optional[_Union[_graph_models_pb2.AuthorizedBadgeHolder, _Mapping]] = ..., vape_detector: _Optional[_Union[_graph_models_pb2.VapeDetector, _Mapping]] = ..., wall: _Optional[_Union[_graph_models_pb2.Wall, _Mapping]] = ..., door: _Optional[_Union[_graph_models_pb2.Door, _Mapping]] = ..., depth: _Optional[int] = ..., kv_map: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GraphResponse(_message.Message):
    __slots__ = ["activity_log", "api_key", "authorized_badge_holder", "badge_reader", "camera", "camera_manufacturer", "camera_model", "campus", "completed", "contact", "coordinate", "customer", "device", "device_cluster", "event", "facility", "floor_plan", "incident", "incident_event", "inference_frame", "level", "location", "mask", "multi_lens_camera", "object_of_interest_tracking_job", "permission", "role", "rule_setting", "shift", "speaker", "system_event", "user", "user_group", "user_session", "vape_detector", "work_hours", "zone"]
    ACTIVITY_LOG_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_BADGE_HOLDER_FIELD_NUMBER: _ClassVar[int]
    BADGE_READER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MODEL_FIELD_NUMBER: _ClassVar[int]
    CAMPUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FLOOR_PLAN_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_EVENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    MULTI_LENS_CAMERA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_OF_INTEREST_TRACKING_JOB_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_EVENT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    USER_GROUP_FIELD_NUMBER: _ClassVar[int]
    USER_SESSION_FIELD_NUMBER: _ClassVar[int]
    VAPE_DETECTOR_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    activity_log: _graph_models_pb2.ActivityLog
    api_key: _graph_models_pb2.APIKey
    authorized_badge_holder: _graph_models_pb2.AuthorizedBadgeHolder
    badge_reader: _graph_models_pb2.BadgeReader
    camera: _graph_models_pb2.Camera
    camera_manufacturer: _graph_models_pb2.CameraManufacturer
    camera_model: _graph_models_pb2.CameraModel
    campus: _graph_models_pb2.Campus
    completed: bool
    contact: _graph_models_pb2.Contact
    coordinate: _graph_models_pb2.Coordinate
    customer: _graph_models_pb2.Customer
    device: _graph_models_pb2.Device
    device_cluster: _graph_models_pb2.DeviceCluster
    event: _graph_models_pb2.Event
    facility: _graph_models_pb2.Facility
    floor_plan: _graph_models_pb2.FloorPlan
    incident: _graph_models_pb2.Incident
    incident_event: _graph_models_pb2.IncidentEvent
    inference_frame: _ai_models_pb2.InferenceFrame
    level: _graph_models_pb2.Level
    location: _graph_models_pb2.Location
    mask: _graph_models_pb2.Mask
    multi_lens_camera: _graph_models_pb2.MultiLensCamera
    object_of_interest_tracking_job: _graph_models_pb2.ObjectOfInterestTrackingJob
    permission: _graph_models_pb2.Permission
    role: _graph_models_pb2.Role
    rule_setting: _graph_models_pb2.RuleSetting
    shift: _graph_models_pb2.Shift
    speaker: _graph_models_pb2.Speaker
    system_event: _graph_models_pb2.SystemEvent
    user: _graph_models_pb2.User
    user_group: _graph_models_pb2.UserGroup
    user_session: _graph_models_pb2.UserSession
    vape_detector: _graph_models_pb2.VapeDetector
    work_hours: _graph_models_pb2.WorkHours
    zone: _graph_models_pb2.Zone
    def __init__(self, user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ..., camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., contact: _Optional[_Union[_graph_models_pb2.Contact, _Mapping]] = ..., incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., api_key: _Optional[_Union[_graph_models_pb2.APIKey, _Mapping]] = ..., user_session: _Optional[_Union[_graph_models_pb2.UserSession, _Mapping]] = ..., level: _Optional[_Union[_graph_models_pb2.Level, _Mapping]] = ..., location: _Optional[_Union[_graph_models_pb2.Location, _Mapping]] = ..., floor_plan: _Optional[_Union[_graph_models_pb2.FloorPlan, _Mapping]] = ..., zone: _Optional[_Union[_graph_models_pb2.Zone, _Mapping]] = ..., event: _Optional[_Union[_graph_models_pb2.Event, _Mapping]] = ..., activity_log: _Optional[_Union[_graph_models_pb2.ActivityLog, _Mapping]] = ..., coordinate: _Optional[_Union[_graph_models_pb2.Coordinate, _Mapping]] = ..., device_cluster: _Optional[_Union[_graph_models_pb2.DeviceCluster, _Mapping]] = ..., rule_setting: _Optional[_Union[_graph_models_pb2.RuleSetting, _Mapping]] = ..., mask: _Optional[_Union[_graph_models_pb2.Mask, _Mapping]] = ..., campus: _Optional[_Union[_graph_models_pb2.Campus, _Mapping]] = ..., speaker: _Optional[_Union[_graph_models_pb2.Speaker, _Mapping]] = ..., multi_lens_camera: _Optional[_Union[_graph_models_pb2.MultiLensCamera, _Mapping]] = ..., work_hours: _Optional[_Union[_graph_models_pb2.WorkHours, _Mapping]] = ..., permission: _Optional[_Union[_graph_models_pb2.Permission, _Mapping]] = ..., role: _Optional[_Union[_graph_models_pb2.Role, _Mapping]] = ..., user_group: _Optional[_Union[_graph_models_pb2.UserGroup, _Mapping]] = ..., shift: _Optional[_Union[_graph_models_pb2.Shift, _Mapping]] = ..., object_of_interest_tracking_job: _Optional[_Union[_graph_models_pb2.ObjectOfInterestTrackingJob, _Mapping]] = ..., inference_frame: _Optional[_Union[_ai_models_pb2.InferenceFrame, _Mapping]] = ..., camera_manufacturer: _Optional[_Union[_graph_models_pb2.CameraManufacturer, _Mapping]] = ..., camera_model: _Optional[_Union[_graph_models_pb2.CameraModel, _Mapping]] = ..., incident_event: _Optional[_Union[_graph_models_pb2.IncidentEvent, _Mapping]] = ..., badge_reader: _Optional[_Union[_graph_models_pb2.BadgeReader, _Mapping]] = ..., system_event: _Optional[_Union[_graph_models_pb2.SystemEvent, _Mapping]] = ..., authorized_badge_holder: _Optional[_Union[_graph_models_pb2.AuthorizedBadgeHolder, _Mapping]] = ..., vape_detector: _Optional[_Union[_graph_models_pb2.VapeDetector, _Mapping]] = ..., completed: bool = ...) -> None: ...

class GraphResponseList(_message.Message):
    __slots__ = ["entities"]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[GraphResponse]
    def __init__(self, entities: _Optional[_Iterable[_Union[GraphResponse, _Mapping]]] = ...) -> None: ...

class IncidentListRequest(_message.Message):
    __slots__ = ["customer_id", "end_time", "facility_ids", "from_timestamp", "query", "rule_ids", "size", "start_index", "start_time", "statuses", "to_timestamp", "user"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    FACILITY_IDS_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RULE_IDS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    end_time: str
    facility_ids: _containers.RepeatedScalarFieldContainer[str]
    from_timestamp: _timestamp_pb2.Timestamp
    query: str
    rule_ids: _containers.RepeatedScalarFieldContainer[str]
    size: int
    start_index: int
    start_time: str
    statuses: _containers.RepeatedScalarFieldContainer[int]
    to_timestamp: _timestamp_pb2.Timestamp
    user: _graph_models_pb2.User
    def __init__(self, start_index: _Optional[int] = ..., size: _Optional[int] = ..., customer_id: _Optional[str] = ..., statuses: _Optional[_Iterable[int]] = ..., query: _Optional[str] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., facility_ids: _Optional[_Iterable[str]] = ..., rule_ids: _Optional[_Iterable[str]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_time: _Optional[str] = ..., end_time: _Optional[str] = ...) -> None: ...

class IncidentSharing(_message.Message):
    __slots__ = ["email", "incident", "phone", "sender"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    email: str
    incident: _graph_models_pb2.Incident
    phone: str
    sender: _graph_models_pb2.User
    def __init__(self, incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., sender: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ["url"]
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class MultiLensCameraList(_message.Message):
    __slots__ = ["cameras"]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.MultiLensCamera]
    def __init__(self, cameras: _Optional[_Iterable[_Union[_graph_models_pb2.MultiLensCamera, _Mapping]]] = ...) -> None: ...

class PagingRequest(_message.Message):
    __slots__ = ["event", "incident", "start_index", "user"]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    event: _graph_models_pb2.IncidentEvent
    incident: _graph_models_pb2.Incident
    start_index: int
    user: _graph_models_pb2.User
    def __init__(self, start_index: _Optional[int] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., event: _Optional[_Union[_graph_models_pb2.IncidentEvent, _Mapping]] = ...) -> None: ...

class PauseRulesRequest(_message.Message):
    __slots__ = ["duration", "facility_id", "rules"]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    duration: int
    facility_id: str
    rules: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.RuleSetting]
    def __init__(self, duration: _Optional[int] = ..., rules: _Optional[_Iterable[_Union[_graph_models_pb2.RuleSetting, _Mapping]]] = ..., facility_id: _Optional[str] = ...) -> None: ...

class RemoteDeviceRequest(_message.Message):
    __slots__ = ["device", "facility"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    device: _graph_models_pb2.Device
    facility: _graph_models_pb2.Facility
    def __init__(self, facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ...) -> None: ...

class RuleList(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.RuleSetting]
    def __init__(self, rules: _Optional[_Iterable[_Union[_graph_models_pb2.RuleSetting, _Mapping]]] = ...) -> None: ...

class SystemEventListRequest(_message.Message):
    __slots__ = ["end_time", "facility_ids", "from_timestamp", "size", "start_index", "start_time", "to_timestamp", "user"]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    FACILITY_IDS_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    end_time: str
    facility_ids: _containers.RepeatedScalarFieldContainer[str]
    from_timestamp: _timestamp_pb2.Timestamp
    size: int
    start_index: int
    start_time: str
    to_timestamp: _timestamp_pb2.Timestamp
    user: _graph_models_pb2.User
    def __init__(self, start_index: _Optional[int] = ..., size: _Optional[int] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., facility_ids: _Optional[_Iterable[str]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_time: _Optional[str] = ..., end_time: _Optional[str] = ...) -> None: ...

class UpdateDeviceClusterRequest(_message.Message):
    __slots__ = ["cluster", "device"]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    cluster: _graph_models_pb2.DeviceCluster
    device: _graph_models_pb2.Device
    def __init__(self, cluster: _Optional[_Union[_graph_models_pb2.DeviceCluster, _Mapping]] = ..., device: _Optional[_Union[_graph_models_pb2.Device, _Mapping]] = ...) -> None: ...

class UpdateIncidentRequest(_message.Message):
    __slots__ = ["description", "incident"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    description: str
    incident: _graph_models_pb2.Incident
    def __init__(self, incident: _Optional[_Union[_graph_models_pb2.Incident, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class VideoPlaybackRequest(_message.Message):
    __slots__ = ["camera", "start_timestamp", "stream_name"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    camera: _graph_models_pb2.Camera
    start_timestamp: _timestamp_pb2.Timestamp
    stream_name: str
    def __init__(self, camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., start_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., stream_name: _Optional[str] = ...) -> None: ...

class VideoPlaybackResponse(_message.Message):
    __slots__ = ["stream_name"]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    stream_name: str
    def __init__(self, stream_name: _Optional[str] = ...) -> None: ...

class ZoneList(_message.Message):
    __slots__ = ["facility_wide_rules", "time_zone", "unassigned_badge_readers", "unassigned_cameras", "unassigned_vape_detectors", "zones"]
    FACILITY_WIDE_RULES_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    UNASSIGNED_BADGE_READERS_FIELD_NUMBER: _ClassVar[int]
    UNASSIGNED_CAMERAS_FIELD_NUMBER: _ClassVar[int]
    UNASSIGNED_VAPE_DETECTORS_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    facility_wide_rules: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.RuleSetting]
    time_zone: str
    unassigned_badge_readers: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.BadgeReader]
    unassigned_cameras: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Camera]
    unassigned_vape_detectors: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.VapeDetector]
    zones: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Zone]
    def __init__(self, zones: _Optional[_Iterable[_Union[_graph_models_pb2.Zone, _Mapping]]] = ..., unassigned_cameras: _Optional[_Iterable[_Union[_graph_models_pb2.Camera, _Mapping]]] = ..., time_zone: _Optional[str] = ..., facility_wide_rules: _Optional[_Iterable[_Union[_graph_models_pb2.RuleSetting, _Mapping]]] = ..., unassigned_badge_readers: _Optional[_Iterable[_Union[_graph_models_pb2.BadgeReader, _Mapping]]] = ..., unassigned_vape_detectors: _Optional[_Iterable[_Union[_graph_models_pb2.VapeDetector, _Mapping]]] = ...) -> None: ...
