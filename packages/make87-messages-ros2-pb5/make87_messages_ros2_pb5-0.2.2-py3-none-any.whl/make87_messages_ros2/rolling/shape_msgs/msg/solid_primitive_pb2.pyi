from make87_messages_ros2.rolling.geometry_msgs.msg import polygon_pb2 as _polygon_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SolidPrimitive(_message.Message):
    __slots__ = ("type", "dimensions", "polygon")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    type: int
    dimensions: _containers.RepeatedScalarFieldContainer[float]
    polygon: _polygon_pb2.Polygon
    def __init__(self, type: _Optional[int] = ..., dimensions: _Optional[_Iterable[float]] = ..., polygon: _Optional[_Union[_polygon_pb2.Polygon, _Mapping]] = ...) -> None: ...
