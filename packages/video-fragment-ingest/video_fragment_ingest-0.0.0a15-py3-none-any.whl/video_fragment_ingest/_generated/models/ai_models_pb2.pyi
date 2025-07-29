from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectedObject(_message.Message):
    __slots__ = ["confidence", "created", "embeddings", "global_track_id", "highlighted", "human_poses", "id", "label", "numeric_tags", "object_class", "orientation", "person", "position_x", "position_y", "reid_embeddings", "string_tags", "track_id", "updated", "x_max", "x_min", "y_max", "y_min"]
    class ObjectClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class NumericTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BACKPACK: DetectedObject.ObjectClass
    BASEBALL_BAT: DetectedObject.ObjectClass
    CAR: DetectedObject.ObjectClass
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    FORKLIFT: DetectedObject.ObjectClass
    GLOBAL_TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTED_FIELD_NUMBER: _ClassVar[int]
    HUMAN_POSES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KNIFE: DetectedObject.ObjectClass
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LONG_GUN: DetectedObject.ObjectClass
    NUMERIC_TAGS_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    PERSON: DetectedObject.ObjectClass
    PERSON_FIELD_NUMBER: _ClassVar[int]
    PHONE: DetectedObject.ObjectClass
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    REID_EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    SUITCASE: DetectedObject.ObjectClass
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: DetectedObject.ObjectClass
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    WEAPON: DetectedObject.ObjectClass
    X_MAX_FIELD_NUMBER: _ClassVar[int]
    X_MIN_FIELD_NUMBER: _ClassVar[int]
    Y_MAX_FIELD_NUMBER: _ClassVar[int]
    Y_MIN_FIELD_NUMBER: _ClassVar[int]
    confidence: float
    created: _timestamp_pb2.Timestamp
    embeddings: Embedding
    global_track_id: str
    highlighted: bool
    human_poses: HumanPose
    id: str
    label: str
    numeric_tags: _containers.ScalarMap[str, float]
    object_class: DetectedObject.ObjectClass
    orientation: float
    person: Person
    position_x: float
    position_y: float
    reid_embeddings: Embedding
    string_tags: _containers.ScalarMap[str, str]
    track_id: str
    updated: _timestamp_pb2.Timestamp
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    def __init__(self, id: _Optional[str] = ..., object_class: _Optional[_Union[DetectedObject.ObjectClass, str]] = ..., confidence: _Optional[float] = ..., x_min: _Optional[float] = ..., y_min: _Optional[float] = ..., x_max: _Optional[float] = ..., y_max: _Optional[float] = ..., track_id: _Optional[str] = ..., global_track_id: _Optional[str] = ..., highlighted: bool = ..., human_poses: _Optional[_Union[HumanPose, _Mapping]] = ..., embeddings: _Optional[_Union[Embedding, _Mapping]] = ..., label: _Optional[str] = ..., person: _Optional[_Union[Person, _Mapping]] = ..., reid_embeddings: _Optional[_Union[Embedding, _Mapping]] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., orientation: _Optional[float] = ..., string_tags: _Optional[_Mapping[str, str]] = ..., numeric_tags: _Optional[_Mapping[str, float]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DetectedObjectList(_message.Message):
    __slots__ = ["id", "objects"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    objects: _containers.RepeatedCompositeFieldContainer[DetectedObject]
    def __init__(self, id: _Optional[str] = ..., objects: _Optional[_Iterable[_Union[DetectedObject, _Mapping]]] = ...) -> None: ...

class Embedding(_message.Message):
    __slots__ = ["embedding", "id"]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    embedding: _containers.RepeatedScalarFieldContainer[float]
    id: str
    def __init__(self, id: _Optional[str] = ..., embedding: _Optional[_Iterable[float]] = ...) -> None: ...

class HumanPose(_message.Message):
    __slots__ = ["body_parts", "confidence", "id"]
    class BodyPart(_message.Message):
        __slots__ = ["confidence", "id", "name", "pos_x", "pos_y"]
        class KeyPoint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        LEFT_ANKLE: HumanPose.BodyPart.KeyPoint
        LEFT_EAR: HumanPose.BodyPart.KeyPoint
        LEFT_ELBOW: HumanPose.BodyPart.KeyPoint
        LEFT_EYE: HumanPose.BodyPart.KeyPoint
        LEFT_HIP: HumanPose.BodyPart.KeyPoint
        LEFT_KNEE: HumanPose.BodyPart.KeyPoint
        LEFT_SHOULDER: HumanPose.BodyPart.KeyPoint
        LEFT_WRIST: HumanPose.BodyPart.KeyPoint
        NAME_FIELD_NUMBER: _ClassVar[int]
        NOSE: HumanPose.BodyPart.KeyPoint
        POS_X_FIELD_NUMBER: _ClassVar[int]
        POS_Y_FIELD_NUMBER: _ClassVar[int]
        RIGHT_ANKLE: HumanPose.BodyPart.KeyPoint
        RIGHT_EAR: HumanPose.BodyPart.KeyPoint
        RIGHT_ELBOW: HumanPose.BodyPart.KeyPoint
        RIGHT_EYE: HumanPose.BodyPart.KeyPoint
        RIGHT_HIP: HumanPose.BodyPart.KeyPoint
        RIGHT_KNEE: HumanPose.BodyPart.KeyPoint
        RIGHT_SHOULDER: HumanPose.BodyPart.KeyPoint
        RIGHT_WRIST: HumanPose.BodyPart.KeyPoint
        UNKNOWN: HumanPose.BodyPart.KeyPoint
        confidence: float
        id: str
        name: HumanPose.BodyPart.KeyPoint
        pos_x: float
        pos_y: float
        def __init__(self, name: _Optional[_Union[HumanPose.BodyPart.KeyPoint, str]] = ..., pos_x: _Optional[float] = ..., pos_y: _Optional[float] = ..., confidence: _Optional[float] = ..., id: _Optional[str] = ...) -> None: ...
    BODY_PARTS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    body_parts: _containers.RepeatedCompositeFieldContainer[HumanPose.BodyPart]
    confidence: float
    id: str
    def __init__(self, id: _Optional[str] = ..., confidence: _Optional[float] = ..., body_parts: _Optional[_Iterable[_Union[HumanPose.BodyPart, _Mapping]]] = ...) -> None: ...

class InferenceFrame(_message.Message):
    __slots__ = ["bucket", "camera_id", "codec", "created", "customer_id", "embeddings", "facility_id", "height", "id", "key", "models", "numeric_tags", "objects", "rotation", "string_tags", "timestamp", "updated", "url", "width"]
    class Codec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class NumericTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class StringTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    FACILITY_ID_FIELD_NUMBER: _ClassVar[int]
    H264: InferenceFrame.Codec
    H265: InferenceFrame.Codec
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_TAGS_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    STRING_TAGS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: InferenceFrame.Codec
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    camera_id: str
    codec: InferenceFrame.Codec
    created: _timestamp_pb2.Timestamp
    customer_id: str
    embeddings: Embedding
    facility_id: str
    height: int
    id: str
    key: str
    models: _containers.RepeatedCompositeFieldContainer[MLModel]
    numeric_tags: _containers.ScalarMap[str, float]
    objects: _containers.RepeatedCompositeFieldContainer[DetectedObject]
    rotation: int
    string_tags: _containers.ScalarMap[str, str]
    timestamp: _timestamp_pb2.Timestamp
    updated: _timestamp_pb2.Timestamp
    url: str
    width: int
    def __init__(self, id: _Optional[str] = ..., camera_id: _Optional[str] = ..., customer_id: _Optional[str] = ..., facility_id: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., objects: _Optional[_Iterable[_Union[DetectedObject, _Mapping]]] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., string_tags: _Optional[_Mapping[str, str]] = ..., numeric_tags: _Optional[_Mapping[str, float]] = ..., url: _Optional[str] = ..., rotation: _Optional[int] = ..., models: _Optional[_Iterable[_Union[MLModel, _Mapping]]] = ..., codec: _Optional[_Union[InferenceFrame.Codec, str]] = ..., embeddings: _Optional[_Union[Embedding, _Mapping]] = ..., created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MLModel(_message.Message):
    __slots__ = ["id", "name", "version"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class Person(_message.Message):
    __slots__ = ["id", "position"]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    id: str
    position: PositionDetails
    def __init__(self, id: _Optional[str] = ..., position: _Optional[_Union[PositionDetails, _Mapping]] = ...) -> None: ...

class PositionDetails(_message.Message):
    __slots__ = ["confidence", "id", "state"]
    class PositionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    FALLEN: PositionDetails.PositionState
    FIGHTING: PositionDetails.PositionState
    HANDS_UP: PositionDetails.PositionState
    ID_FIELD_NUMBER: _ClassVar[int]
    SITTING: PositionDetails.PositionState
    STANDING: PositionDetails.PositionState
    STATE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: PositionDetails.PositionState
    WALKING: PositionDetails.PositionState
    WORKING_OUT: PositionDetails.PositionState
    confidence: float
    id: str
    state: PositionDetails.PositionState
    def __init__(self, id: _Optional[str] = ..., state: _Optional[_Union[PositionDetails.PositionState, str]] = ..., confidence: _Optional[float] = ...) -> None: ...

class Tracker(_message.Message):
    __slots__ = ["id", "mode", "tracker_id"]
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACTIVE: Tracker.Mode
    ID_FIELD_NUMBER: _ClassVar[int]
    INACTIVE: Tracker.Mode
    MODE_FIELD_NUMBER: _ClassVar[int]
    TENTATIVE: Tracker.Mode
    TERMINATED: Tracker.Mode
    TRACKER_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Tracker.Mode
    id: str
    mode: Tracker.Mode
    tracker_id: int
    def __init__(self, id: _Optional[str] = ..., tracker_id: _Optional[int] = ..., mode: _Optional[_Union[Tracker.Mode, str]] = ...) -> None: ...
