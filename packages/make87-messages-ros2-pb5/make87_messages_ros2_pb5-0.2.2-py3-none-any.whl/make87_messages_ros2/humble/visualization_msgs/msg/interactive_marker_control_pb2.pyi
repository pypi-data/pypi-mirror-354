from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.humble.visualization_msgs.msg import marker_pb2 as _marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InteractiveMarkerControl(_message.Message):
    __slots__ = ("header", "name", "orientation", "orientation_mode", "interaction_mode", "always_visible", "markers", "independent_marker_orientation", "description")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_MODE_FIELD_NUMBER: _ClassVar[int]
    INTERACTION_MODE_FIELD_NUMBER: _ClassVar[int]
    ALWAYS_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    INDEPENDENT_MARKER_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    orientation: _quaternion_pb2.Quaternion
    orientation_mode: int
    interaction_mode: int
    always_visible: bool
    markers: _containers.RepeatedCompositeFieldContainer[_marker_pb2.Marker]
    independent_marker_orientation: bool
    description: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., orientation_mode: _Optional[int] = ..., interaction_mode: _Optional[int] = ..., always_visible: bool = ..., markers: _Optional[_Iterable[_Union[_marker_pb2.Marker, _Mapping]]] = ..., independent_marker_orientation: bool = ..., description: _Optional[str] = ...) -> None: ...
