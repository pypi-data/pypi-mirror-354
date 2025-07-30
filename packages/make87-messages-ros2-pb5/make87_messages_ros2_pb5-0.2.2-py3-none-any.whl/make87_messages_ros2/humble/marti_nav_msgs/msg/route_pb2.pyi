from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_common_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import route_point_pb2 as _route_point_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Route(_message.Message):
    __slots__ = ("header", "ros2_header", "route_points", "properties")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_POINTS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    route_points: _containers.RepeatedCompositeFieldContainer[_route_point_pb2.RoutePoint]
    properties: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., route_points: _Optional[_Iterable[_Union[_route_point_pb2.RoutePoint, _Mapping]]] = ..., properties: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
