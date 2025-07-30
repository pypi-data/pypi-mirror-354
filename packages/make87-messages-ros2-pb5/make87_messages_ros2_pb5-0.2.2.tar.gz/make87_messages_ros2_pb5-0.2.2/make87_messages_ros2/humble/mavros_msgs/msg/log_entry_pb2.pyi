from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogEntry(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "num_logs", "last_log_num", "time_utc", "size")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NUM_LOGS_FIELD_NUMBER: _ClassVar[int]
    LAST_LOG_NUM_FIELD_NUMBER: _ClassVar[int]
    TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    num_logs: int
    last_log_num: int
    time_utc: _time_pb2.Time
    size: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., num_logs: _Optional[int] = ..., last_log_num: _Optional[int] = ..., time_utc: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., size: _Optional[int] = ...) -> None: ...
