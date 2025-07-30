from make87_messages_ros2.jazzy.rtabmap_msgs.msg import landmark_detection_pb2 as _landmark_detection_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandmarkDetections(_message.Message):
    __slots__ = ("header", "landmarks")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDMARKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    landmarks: _containers.RepeatedCompositeFieldContainer[_landmark_detection_pb2.LandmarkDetection]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., landmarks: _Optional[_Iterable[_Union[_landmark_detection_pb2.LandmarkDetection, _Mapping]]] = ...) -> None: ...
