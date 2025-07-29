from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalyticsReportRequest(_message.Message):
    __slots__ = ["email_override", "facilities", "from_timestamp", "id", "to_timestamp", "user"]
    EMAIL_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    email_override: str
    facilities: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Facility]
    from_timestamp: _timestamp_pb2.Timestamp
    id: str
    to_timestamp: _timestamp_pb2.Timestamp
    user: _graph_models_pb2.User
    def __init__(self, id: _Optional[str] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., facilities: _Optional[_Iterable[_Union[_graph_models_pb2.Facility, _Mapping]]] = ..., email_override: _Optional[str] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentsAvgResolveTimeRequest(_message.Message):
    __slots__ = ["customer", "facilities", "from_timestamp", "to_timestamp"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    facilities: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Facility]
    from_timestamp: _timestamp_pb2.Timestamp
    to_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, facilities: _Optional[_Iterable[_Union[_graph_models_pb2.Facility, _Mapping]]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentsAvgResolveTimeResponse(_message.Message):
    __slots__ = ["avg", "closed_incidents_count"]
    AVG_FIELD_NUMBER: _ClassVar[int]
    CLOSED_INCIDENTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    avg: float
    closed_incidents_count: int
    def __init__(self, avg: _Optional[float] = ..., closed_incidents_count: _Optional[int] = ...) -> None: ...

class IncidentsHistogramRequest(_message.Message):
    __slots__ = ["after_key", "customer", "facilities", "from_timestamp", "max_buckets", "to_timestamp"]
    AFTER_KEY_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MAX_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    after_key: IncidentsHistogramResponse.Bucket.Key
    customer: _graph_models_pb2.Customer
    facilities: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Facility]
    from_timestamp: _timestamp_pb2.Timestamp
    max_buckets: int
    to_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, facilities: _Optional[_Iterable[_Union[_graph_models_pb2.Facility, _Mapping]]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., after_key: _Optional[_Union[IncidentsHistogramResponse.Bucket.Key, _Mapping]] = ..., max_buckets: _Optional[int] = ...) -> None: ...

class IncidentsHistogramResponse(_message.Message):
    __slots__ = ["after_key", "buckets"]
    class Bucket(_message.Message):
        __slots__ = ["count", "key"]
        class Key(_message.Message):
            __slots__ = ["date", "facility_id", "trigger_rule_id"]
            DATE_FIELD_NUMBER: _ClassVar[int]
            FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
            TRIGGER_RULE_ID_FIELD_NUMBER: _ClassVar[int]
            date: str
            facility_id: str
            trigger_rule_id: str
            def __init__(self, date: _Optional[str] = ..., trigger_rule_id: _Optional[str] = ..., facility_id: _Optional[str] = ...) -> None: ...
        COUNT_FIELD_NUMBER: _ClassVar[int]
        KEY_FIELD_NUMBER: _ClassVar[int]
        count: int
        key: IncidentsHistogramResponse.Bucket.Key
        def __init__(self, key: _Optional[_Union[IncidentsHistogramResponse.Bucket.Key, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...
    AFTER_KEY_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    after_key: IncidentsHistogramResponse.Bucket.Key
    buckets: _containers.RepeatedCompositeFieldContainer[IncidentsHistogramResponse.Bucket]
    def __init__(self, after_key: _Optional[_Union[IncidentsHistogramResponse.Bucket.Key, _Mapping]] = ..., buckets: _Optional[_Iterable[_Union[IncidentsHistogramResponse.Bucket, _Mapping]]] = ...) -> None: ...

class IncidentsOverviewRequest(_message.Message):
    __slots__ = ["customer", "facilities", "from_timestamp", "to_timestamp"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    FACILITIES_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    facilities: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Facility]
    from_timestamp: _timestamp_pb2.Timestamp
    to_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, facilities: _Optional[_Iterable[_Union[_graph_models_pb2.Facility, _Mapping]]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IncidentsOverviewResponse(_message.Message):
    __slots__ = ["open_incidents", "open_incidents_total_count"]
    OPEN_INCIDENTS_FIELD_NUMBER: _ClassVar[int]
    OPEN_INCIDENTS_TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    open_incidents: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.Incident]
    open_incidents_total_count: int
    def __init__(self, open_incidents_total_count: _Optional[int] = ..., open_incidents: _Optional[_Iterable[_Union[_graph_models_pb2.Incident, _Mapping]]] = ...) -> None: ...

class OccupancyHistogramByZoneTypeRequest(_message.Message):
    __slots__ = ["facility", "from_timestamp", "to_timestamp", "zone_types"]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ZONE_TYPES_FIELD_NUMBER: _ClassVar[int]
    facility: _graph_models_pb2.Facility
    from_timestamp: _timestamp_pb2.Timestamp
    to_timestamp: _timestamp_pb2.Timestamp
    zone_types: _containers.RepeatedScalarFieldContainer[_graph_models_pb2.Zone.ZoneType]
    def __init__(self, facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., zone_types: _Optional[_Iterable[_Union[_graph_models_pb2.Zone.ZoneType, str]]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OccupancyHistogramRequest(_message.Message):
    __slots__ = ["camera", "facility", "from_timestamp", "level", "location", "to_timestamp"]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TO_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    camera: _graph_models_pb2.Camera
    facility: _graph_models_pb2.Facility
    from_timestamp: _timestamp_pb2.Timestamp
    level: _graph_models_pb2.Level
    location: _graph_models_pb2.Location
    to_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., level: _Optional[_Union[_graph_models_pb2.Level, _Mapping]] = ..., location: _Optional[_Union[_graph_models_pb2.Location, _Mapping]] = ..., camera: _Optional[_Union[_graph_models_pb2.Camera, _Mapping]] = ..., from_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., to_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OccupancyHistogramResponse(_message.Message):
    __slots__ = ["buckets"]
    class Bucket(_message.Message):
        __slots__ = ["count", "timestamp"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        count: int
        timestamp: _timestamp_pb2.Timestamp
        def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedCompositeFieldContainer[OccupancyHistogramResponse.Bucket]
    def __init__(self, buckets: _Optional[_Iterable[_Union[OccupancyHistogramResponse.Bucket, _Mapping]]] = ...) -> None: ...
