from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Builtins(_message.Message):
    __slots__ = ("header", "duration_value", "time_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    duration_value: _duration_pb2.Duration
    time_value: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., duration_value: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., time_value: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
