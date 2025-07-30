from make87_messages_ros2.jazzy.geometry_msgs.msg import polygon_instance_pb2 as _polygon_instance_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolygonInstanceStamped(_message.Message):
    __slots__ = ("header", "polygon")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    polygon: _polygon_instance_pb2.PolygonInstance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., polygon: _Optional[_Union[_polygon_instance_pb2.PolygonInstance, _Mapping]] = ...) -> None: ...
