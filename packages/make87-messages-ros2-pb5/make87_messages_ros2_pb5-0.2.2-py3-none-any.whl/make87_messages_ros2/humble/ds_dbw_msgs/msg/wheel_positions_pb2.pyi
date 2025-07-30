from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelPositions(_message.Message):
    __slots__ = ("header", "ros2_header", "front_left", "front_right", "rear_left", "rear_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    REAR_LEFT_FIELD_NUMBER: _ClassVar[int]
    REAR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    front_left: int
    front_right: int
    rear_left: int
    rear_right: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., front_left: _Optional[int] = ..., front_right: _Optional[int] = ..., rear_left: _Optional[int] = ..., rear_right: _Optional[int] = ...) -> None: ...
