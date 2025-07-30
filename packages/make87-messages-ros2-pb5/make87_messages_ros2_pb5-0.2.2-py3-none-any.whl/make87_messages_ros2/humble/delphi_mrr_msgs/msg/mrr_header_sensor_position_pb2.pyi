from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderSensorPosition(_message.Message):
    __slots__ = ("header", "ros2_header", "can_sensor_polarity", "can_sensor_lat_offset", "can_sensor_long_offset", "can_sensor_hangle_offset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_POLARITY_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_LAT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_LONG_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_HANGLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_sensor_polarity: bool
    can_sensor_lat_offset: float
    can_sensor_long_offset: float
    can_sensor_hangle_offset: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_sensor_polarity: bool = ..., can_sensor_lat_offset: _Optional[float] = ..., can_sensor_long_offset: _Optional[float] = ..., can_sensor_hangle_offset: _Optional[float] = ...) -> None: ...
