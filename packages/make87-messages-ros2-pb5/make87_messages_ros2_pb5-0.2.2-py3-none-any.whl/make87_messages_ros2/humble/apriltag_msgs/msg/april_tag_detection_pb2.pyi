from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.apriltag_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AprilTagDetection(_message.Message):
    __slots__ = ("header", "family", "id", "hamming", "goodness", "decision_margin", "centre", "corners", "homography")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    HAMMING_FIELD_NUMBER: _ClassVar[int]
    GOODNESS_FIELD_NUMBER: _ClassVar[int]
    DECISION_MARGIN_FIELD_NUMBER: _ClassVar[int]
    CENTRE_FIELD_NUMBER: _ClassVar[int]
    CORNERS_FIELD_NUMBER: _ClassVar[int]
    HOMOGRAPHY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    family: str
    id: int
    hamming: int
    goodness: float
    decision_margin: float
    centre: _point_pb2.Point
    corners: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    homography: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., family: _Optional[str] = ..., id: _Optional[int] = ..., hamming: _Optional[int] = ..., goodness: _Optional[float] = ..., decision_margin: _Optional[float] = ..., centre: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., corners: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., homography: _Optional[_Iterable[float]] = ...) -> None: ...
