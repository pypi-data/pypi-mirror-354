from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lgsvl_msgs.msg import detection2_d_pb2 as _detection2_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Detection2DArray(_message.Message):
    __slots__ = ("header", "ros2_header", "detections")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    detections: _containers.RepeatedCompositeFieldContainer[_detection2_d_pb2.Detection2D]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., detections: _Optional[_Iterable[_Union[_detection2_d_pb2.Detection2D, _Mapping]]] = ...) -> None: ...
