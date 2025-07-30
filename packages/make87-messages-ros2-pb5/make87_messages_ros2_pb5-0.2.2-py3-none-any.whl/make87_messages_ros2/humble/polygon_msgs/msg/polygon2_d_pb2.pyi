from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.polygon_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon2D(_message.Message):
    __slots__ = ("header", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    points: _containers.RepeatedCompositeFieldContainer[_point2_d_pb2.Point2D]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_point2_d_pb2.Point2D, _Mapping]]] = ...) -> None: ...
