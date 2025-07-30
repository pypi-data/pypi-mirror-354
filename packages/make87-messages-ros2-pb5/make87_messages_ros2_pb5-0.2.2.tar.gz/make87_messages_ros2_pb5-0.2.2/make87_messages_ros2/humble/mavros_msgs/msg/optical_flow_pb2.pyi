from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpticalFlow(_message.Message):
    __slots__ = ("header", "ros2_header", "flow", "flow_comp_m", "quality", "ground_distance", "flow_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    FLOW_COMP_M_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    GROUND_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    FLOW_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    flow: _vector3_pb2.Vector3
    flow_comp_m: _vector3_pb2.Vector3
    quality: int
    ground_distance: float
    flow_rate: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., flow: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., flow_comp_m: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., quality: _Optional[int] = ..., ground_distance: _Optional[float] = ..., flow_rate: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
