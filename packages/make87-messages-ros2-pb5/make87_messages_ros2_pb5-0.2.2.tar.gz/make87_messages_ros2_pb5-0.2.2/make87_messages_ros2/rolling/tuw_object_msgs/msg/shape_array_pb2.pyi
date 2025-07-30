from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_object_msgs.msg import shape_pb2 as _shape_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShapeArray(_message.Message):
    __slots__ = ("header", "shapes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    shapes: _containers.RepeatedCompositeFieldContainer[_shape_pb2.Shape]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., shapes: _Optional[_Iterable[_Union[_shape_pb2.Shape, _Mapping]]] = ...) -> None: ...
