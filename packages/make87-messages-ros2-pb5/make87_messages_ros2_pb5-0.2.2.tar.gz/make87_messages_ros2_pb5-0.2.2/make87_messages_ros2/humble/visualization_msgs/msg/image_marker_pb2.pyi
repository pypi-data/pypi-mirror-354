from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageMarker(_message.Message):
    __slots__ = ("header", "ros2_header", "ns", "id", "type", "action", "position", "scale", "outline_color", "filled", "fill_color", "lifetime", "points", "outline_colors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_COLOR_FIELD_NUMBER: _ClassVar[int]
    FILLED_FIELD_NUMBER: _ClassVar[int]
    FILL_COLOR_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_COLORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ns: str
    id: int
    type: int
    action: int
    position: _point_pb2.Point
    scale: float
    outline_color: _color_rgba_pb2.ColorRGBA
    filled: int
    fill_color: _color_rgba_pb2.ColorRGBA
    lifetime: _duration_pb2.Duration
    points: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    outline_colors: _containers.RepeatedCompositeFieldContainer[_color_rgba_pb2.ColorRGBA]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ns: _Optional[str] = ..., id: _Optional[int] = ..., type: _Optional[int] = ..., action: _Optional[int] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., scale: _Optional[float] = ..., outline_color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., filled: _Optional[int] = ..., fill_color: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., lifetime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., outline_colors: _Optional[_Iterable[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]]] = ...) -> None: ...
