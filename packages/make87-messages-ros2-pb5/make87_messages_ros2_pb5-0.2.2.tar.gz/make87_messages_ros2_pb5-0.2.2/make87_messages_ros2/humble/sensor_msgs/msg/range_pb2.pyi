from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Range(_message.Message):
    __slots__ = ("header", "ros2_header", "radiation_type", "field_of_view", "min_range", "max_range", "range")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    RADIATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELD_OF_VIEW_FIELD_NUMBER: _ClassVar[int]
    MIN_RANGE_FIELD_NUMBER: _ClassVar[int]
    MAX_RANGE_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    radiation_type: int
    field_of_view: float
    min_range: float
    max_range: float
    range: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., radiation_type: _Optional[int] = ..., field_of_view: _Optional[float] = ..., min_range: _Optional[float] = ..., max_range: _Optional[float] = ..., range: _Optional[float] = ...) -> None: ...
