from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleControl(_message.Message):
    __slots__ = ("header", "ros2_header", "engine", "gear", "steering", "throttle", "brake", "steering_position", "gb_position")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    STEERING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    STEERING_POSITION_FIELD_NUMBER: _ClassVar[int]
    GB_POSITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    engine: int
    gear: int
    steering: float
    throttle: float
    brake: float
    steering_position: int
    gb_position: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., engine: _Optional[int] = ..., gear: _Optional[int] = ..., steering: _Optional[float] = ..., throttle: _Optional[float] = ..., brake: _Optional[float] = ..., steering_position: _Optional[int] = ..., gb_position: _Optional[int] = ...) -> None: ...
