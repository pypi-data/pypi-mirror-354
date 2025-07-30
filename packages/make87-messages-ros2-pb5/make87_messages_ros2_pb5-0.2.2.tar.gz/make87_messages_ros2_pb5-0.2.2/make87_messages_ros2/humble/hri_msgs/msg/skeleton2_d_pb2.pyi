from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.hri_msgs.msg import normalized_point_of_interest2_d_pb2 as _normalized_point_of_interest2_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Skeleton2D(_message.Message):
    __slots__ = ("header", "ros2_header", "skeleton")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SKELETON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    skeleton: _containers.RepeatedCompositeFieldContainer[_normalized_point_of_interest2_d_pb2.NormalizedPointOfInterest2D]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., skeleton: _Optional[_Iterable[_Union[_normalized_point_of_interest2_d_pb2.NormalizedPointOfInterest2D, _Mapping]]] = ...) -> None: ...
