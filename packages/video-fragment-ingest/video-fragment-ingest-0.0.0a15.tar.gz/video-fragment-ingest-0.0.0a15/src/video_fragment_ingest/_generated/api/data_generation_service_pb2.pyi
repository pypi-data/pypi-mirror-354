from google.protobuf import empty_pb2 as _empty_pb2
from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerationRequest(_message.Message):
    __slots__ = ["record_count"]
    RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    record_count: int
    def __init__(self, record_count: _Optional[int] = ...) -> None: ...

class TestInferenceFrameStream(_message.Message):
    __slots__ = ["camera_id", "duration", "show_object_at_time", "test_mode"]
    class TestMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    MEDICAL: TestInferenceFrameStream.TestMode
    SHOW_OBJECT_AT_TIME_FIELD_NUMBER: _ClassVar[int]
    TEST_MODE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_TEST_CASE: TestInferenceFrameStream.TestMode
    WEAPON: TestInferenceFrameStream.TestMode
    camera_id: str
    duration: int
    show_object_at_time: _containers.RepeatedScalarFieldContainer[int]
    test_mode: TestInferenceFrameStream.TestMode
    def __init__(self, duration: _Optional[int] = ..., show_object_at_time: _Optional[_Iterable[int]] = ..., camera_id: _Optional[str] = ..., test_mode: _Optional[_Union[TestInferenceFrameStream.TestMode, str]] = ...) -> None: ...
