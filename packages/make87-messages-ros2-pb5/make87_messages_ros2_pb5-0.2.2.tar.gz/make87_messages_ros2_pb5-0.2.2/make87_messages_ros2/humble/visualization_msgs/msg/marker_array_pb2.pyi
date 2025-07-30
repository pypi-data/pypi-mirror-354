from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.visualization_msgs.msg import marker_pb2 as _marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkerArray(_message.Message):
    __slots__ = ("header", "markers")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    markers: _containers.RepeatedCompositeFieldContainer[_marker_pb2.Marker]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., markers: _Optional[_Iterable[_Union[_marker_pb2.Marker, _Mapping]]] = ...) -> None: ...
