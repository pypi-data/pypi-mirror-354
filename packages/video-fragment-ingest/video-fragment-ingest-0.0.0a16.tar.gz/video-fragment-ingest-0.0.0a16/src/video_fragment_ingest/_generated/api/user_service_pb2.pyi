from google.protobuf import empty_pb2 as _empty_pb2
from models import graph_models_pb2 as _graph_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssignEscalationPolicyRequest(_message.Message):
    __slots__ = ["facility", "policy", "rule_setting", "zone"]
    FACILITY_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    facility: _graph_models_pb2.Facility
    policy: _graph_models_pb2.EscalationPolicy
    rule_setting: _graph_models_pb2.RuleSetting
    zone: _graph_models_pb2.Zone
    def __init__(self, policy: _Optional[_Union[_graph_models_pb2.EscalationPolicy, _Mapping]] = ..., facility: _Optional[_Union[_graph_models_pb2.Facility, _Mapping]] = ..., zone: _Optional[_Union[_graph_models_pb2.Zone, _Mapping]] = ..., rule_setting: _Optional[_Union[_graph_models_pb2.RuleSetting, _Mapping]] = ...) -> None: ...

class CheckTokenRequest(_message.Message):
    __slots__ = ["secret_token"]
    SECRET_TOKEN_FIELD_NUMBER: _ClassVar[int]
    secret_token: str
    def __init__(self, secret_token: _Optional[str] = ...) -> None: ...

class CheckTokenResponse(_message.Message):
    __slots__ = ["customer", "token", "valid"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    token: _graph_models_pb2.Token
    valid: bool
    def __init__(self, valid: bool = ..., token: _Optional[_Union[_graph_models_pb2.Token, _Mapping]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ...) -> None: ...

class CreateTokenRequest(_message.Message):
    __slots__ = ["customer", "token", "user"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    token: _graph_models_pb2.Token
    user: _graph_models_pb2.User
    def __init__(self, token: _Optional[_Union[_graph_models_pb2.Token, _Mapping]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ..., user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ...) -> None: ...

class EscalationPolicies(_message.Message):
    __slots__ = ["policies"]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.EscalationPolicy]
    def __init__(self, policies: _Optional[_Iterable[_Union[_graph_models_pb2.EscalationPolicy, _Mapping]]] = ...) -> None: ...

class EscalationPolicyWithOnCallUsers(_message.Message):
    __slots__ = ["on_call_users", "policy"]
    ON_CALL_USERS_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    on_call_users: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.User]
    policy: _graph_models_pb2.EscalationPolicy
    def __init__(self, policy: _Optional[_Union[_graph_models_pb2.EscalationPolicy, _Mapping]] = ..., on_call_users: _Optional[_Iterable[_Union[_graph_models_pb2.User, _Mapping]]] = ...) -> None: ...

class SAMLUserRequest(_message.Message):
    __slots__ = ["email"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class SAMLUserResponse(_message.Message):
    __slots__ = ["customer_name", "provider"]
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    customer_name: str
    provider: str
    def __init__(self, provider: _Optional[str] = ..., customer_name: _Optional[str] = ...) -> None: ...

class SetMFAOptionsRequest(_message.Message):
    __slots__ = ["sms_enabled", "sms_preferred", "totp_enabled", "totp_preferred", "user"]
    SMS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SMS_PREFERRED_FIELD_NUMBER: _ClassVar[int]
    TOTP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TOTP_PREFERRED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    sms_enabled: bool
    sms_preferred: bool
    totp_enabled: bool
    totp_preferred: bool
    user: _graph_models_pb2.User
    def __init__(self, user: _Optional[_Union[_graph_models_pb2.User, _Mapping]] = ..., sms_enabled: bool = ..., sms_preferred: bool = ..., totp_enabled: bool = ..., totp_preferred: bool = ...) -> None: ...

class TokenGeneratedResponse(_message.Message):
    __slots__ = ["secret_token", "token"]
    SECRET_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    secret_token: str
    token: _graph_models_pb2.Token
    def __init__(self, token: _Optional[_Union[_graph_models_pb2.Token, _Mapping]] = ..., secret_token: _Optional[str] = ...) -> None: ...

class UserList(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.User]
    def __init__(self, users: _Optional[_Iterable[_Union[_graph_models_pb2.User, _Mapping]]] = ...) -> None: ...

class UserPermissionResponse(_message.Message):
    __slots__ = ["groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.UserGroup]
    def __init__(self, groups: _Optional[_Iterable[_Union[_graph_models_pb2.UserGroup, _Mapping]]] = ...) -> None: ...

class WorkShift(_message.Message):
    __slots__ = ["customer", "shift", "users", "work_hours"]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
    customer: _graph_models_pb2.Customer
    shift: _graph_models_pb2.Shift
    users: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.User]
    work_hours: _graph_models_pb2.WorkHours
    def __init__(self, shift: _Optional[_Union[_graph_models_pb2.Shift, _Mapping]] = ..., work_hours: _Optional[_Union[_graph_models_pb2.WorkHours, _Mapping]] = ..., users: _Optional[_Iterable[_Union[_graph_models_pb2.User, _Mapping]]] = ..., customer: _Optional[_Union[_graph_models_pb2.Customer, _Mapping]] = ...) -> None: ...

class WorkShiftWithUser(_message.Message):
    __slots__ = ["shift", "work_hours_with_user"]
    class WorkHoursWithUser(_message.Message):
        __slots__ = ["users", "work_hours"]
        USERS_FIELD_NUMBER: _ClassVar[int]
        WORK_HOURS_FIELD_NUMBER: _ClassVar[int]
        users: _containers.RepeatedCompositeFieldContainer[_graph_models_pb2.User]
        work_hours: _graph_models_pb2.WorkHours
        def __init__(self, work_hours: _Optional[_Union[_graph_models_pb2.WorkHours, _Mapping]] = ..., users: _Optional[_Iterable[_Union[_graph_models_pb2.User, _Mapping]]] = ...) -> None: ...
    SHIFT_FIELD_NUMBER: _ClassVar[int]
    WORK_HOURS_WITH_USER_FIELD_NUMBER: _ClassVar[int]
    shift: _graph_models_pb2.Shift
    work_hours_with_user: _containers.RepeatedCompositeFieldContainer[WorkShiftWithUser.WorkHoursWithUser]
    def __init__(self, shift: _Optional[_Union[_graph_models_pb2.Shift, _Mapping]] = ..., work_hours_with_user: _Optional[_Iterable[_Union[WorkShiftWithUser.WorkHoursWithUser, _Mapping]]] = ...) -> None: ...

class WorkShifts(_message.Message):
    __slots__ = ["work_shifts"]
    WORK_SHIFTS_FIELD_NUMBER: _ClassVar[int]
    work_shifts: _containers.RepeatedCompositeFieldContainer[WorkShiftWithUser]
    def __init__(self, work_shifts: _Optional[_Iterable[_Union[WorkShiftWithUser, _Mapping]]] = ...) -> None: ...
