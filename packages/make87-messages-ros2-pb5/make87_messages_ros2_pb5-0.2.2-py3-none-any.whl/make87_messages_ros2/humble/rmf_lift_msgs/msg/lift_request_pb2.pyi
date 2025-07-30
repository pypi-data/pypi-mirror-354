from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LiftRequest(_message.Message):
    __slots__ = ("header", "lift_name", "request_time", "session_id", "request_type", "destination_floor", "door_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FLOOR_FIELD_NUMBER: _ClassVar[int]
    DOOR_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lift_name: str
    request_time: _time_pb2.Time
    session_id: str
    request_type: int
    destination_floor: str
    door_state: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lift_name: _Optional[str] = ..., request_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., session_id: _Optional[str] = ..., request_type: _Optional[int] = ..., destination_floor: _Optional[str] = ..., door_state: _Optional[int] = ...) -> None: ...
