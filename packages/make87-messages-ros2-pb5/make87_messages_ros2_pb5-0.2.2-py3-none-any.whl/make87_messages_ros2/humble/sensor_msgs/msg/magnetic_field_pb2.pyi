from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MagneticField(_message.Message):
    __slots__ = ("header", "ros2_header", "magnetic_field", "magnetic_field_covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MAGNETIC_FIELD_FIELD_NUMBER: _ClassVar[int]
    MAGNETIC_FIELD_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    magnetic_field: _vector3_pb2.Vector3
    magnetic_field_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., magnetic_field: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., magnetic_field_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
