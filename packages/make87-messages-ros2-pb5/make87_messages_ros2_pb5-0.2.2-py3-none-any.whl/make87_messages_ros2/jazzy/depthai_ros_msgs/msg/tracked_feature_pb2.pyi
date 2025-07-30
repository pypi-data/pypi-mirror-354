from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackedFeature(_message.Message):
    __slots__ = ("header", "position", "id", "age", "harris_score", "tracking_error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HARRIS_SCORE_FIELD_NUMBER: _ClassVar[int]
    TRACKING_ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _point_pb2.Point
    id: int
    age: int
    harris_score: float
    tracking_error: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., id: _Optional[int] = ..., age: _Optional[int] = ..., harris_score: _Optional[float] = ..., tracking_error: _Optional[float] = ...) -> None: ...
