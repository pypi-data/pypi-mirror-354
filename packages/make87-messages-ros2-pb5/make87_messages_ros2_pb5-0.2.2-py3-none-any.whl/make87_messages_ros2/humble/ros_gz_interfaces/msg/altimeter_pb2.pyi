from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Altimeter(_message.Message):
    __slots__ = ("header", "ros2_header", "vertical_position", "vertical_velocity", "vertical_reference")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_POSITION_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    vertical_position: float
    vertical_velocity: float
    vertical_reference: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., vertical_position: _Optional[float] = ..., vertical_velocity: _Optional[float] = ..., vertical_reference: _Optional[float] = ...) -> None: ...
