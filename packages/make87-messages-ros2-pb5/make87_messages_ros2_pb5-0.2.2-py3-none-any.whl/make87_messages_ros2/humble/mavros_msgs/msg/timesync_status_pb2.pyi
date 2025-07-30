from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimesyncStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "remote_timestamp_ns", "observed_offset_ns", "estimated_offset_ns", "round_trip_time_ms")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    REMOTE_TIMESTAMP_NS_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_OFFSET_NS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_OFFSET_NS_FIELD_NUMBER: _ClassVar[int]
    ROUND_TRIP_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    remote_timestamp_ns: int
    observed_offset_ns: int
    estimated_offset_ns: int
    round_trip_time_ms: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., remote_timestamp_ns: _Optional[int] = ..., observed_offset_ns: _Optional[int] = ..., estimated_offset_ns: _Optional[int] = ..., round_trip_time_ms: _Optional[float] = ...) -> None: ...
