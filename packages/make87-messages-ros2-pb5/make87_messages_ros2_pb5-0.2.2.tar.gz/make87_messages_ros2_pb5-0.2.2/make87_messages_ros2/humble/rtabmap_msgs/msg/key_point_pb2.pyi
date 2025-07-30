from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import point2f_pb2 as _point2f_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KeyPoint(_message.Message):
    __slots__ = ("header", "pt", "size", "angle", "response", "octave", "class_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PT_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    OCTAVE_FIELD_NUMBER: _ClassVar[int]
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pt: _point2f_pb2.Point2f
    size: float
    angle: float
    response: float
    octave: int
    class_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pt: _Optional[_Union[_point2f_pb2.Point2f, _Mapping]] = ..., size: _Optional[float] = ..., angle: _Optional[float] = ..., response: _Optional[float] = ..., octave: _Optional[int] = ..., class_id: _Optional[int] = ...) -> None: ...
