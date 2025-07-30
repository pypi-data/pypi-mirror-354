from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Longitudinal(_message.Message):
    __slots__ = ("header", "stamp", "control_time", "velocity", "acceleration", "jerk", "is_defined_acceleration", "is_defined_jerk")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TIME_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    JERK_FIELD_NUMBER: _ClassVar[int]
    IS_DEFINED_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    IS_DEFINED_JERK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    control_time: _time_pb2.Time
    velocity: float
    acceleration: float
    jerk: float
    is_defined_acceleration: bool
    is_defined_jerk: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., control_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., velocity: _Optional[float] = ..., acceleration: _Optional[float] = ..., jerk: _Optional[float] = ..., is_defined_acceleration: bool = ..., is_defined_jerk: bool = ...) -> None: ...
