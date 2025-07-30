from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelocityReport(_message.Message):
    __slots__ = ("header", "ros2_header", "longitudinal_velocity", "lateral_velocity", "heading_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    LATERAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    HEADING_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    longitudinal_velocity: float
    lateral_velocity: float
    heading_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., longitudinal_velocity: _Optional[float] = ..., lateral_velocity: _Optional[float] = ..., heading_rate: _Optional[float] = ...) -> None: ...
