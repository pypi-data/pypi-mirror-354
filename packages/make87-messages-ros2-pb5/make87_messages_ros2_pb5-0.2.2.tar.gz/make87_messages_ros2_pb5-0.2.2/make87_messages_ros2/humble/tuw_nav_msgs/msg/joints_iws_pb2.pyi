from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointsIWS(_message.Message):
    __slots__ = ("header", "ros2_header", "type_steering", "type_revolute", "steering", "revolute")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_STEERING_FIELD_NUMBER: _ClassVar[int]
    TYPE_REVOLUTE_FIELD_NUMBER: _ClassVar[int]
    STEERING_FIELD_NUMBER: _ClassVar[int]
    REVOLUTE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    type_steering: str
    type_revolute: str
    steering: _containers.RepeatedScalarFieldContainer[float]
    revolute: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., type_steering: _Optional[str] = ..., type_revolute: _Optional[str] = ..., steering: _Optional[_Iterable[float]] = ..., revolute: _Optional[_Iterable[float]] = ...) -> None: ...
