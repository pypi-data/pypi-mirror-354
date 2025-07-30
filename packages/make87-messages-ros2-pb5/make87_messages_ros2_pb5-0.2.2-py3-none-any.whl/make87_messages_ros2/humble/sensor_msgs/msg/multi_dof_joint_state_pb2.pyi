from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiDOFJointState(_message.Message):
    __slots__ = ("header", "ros2_header", "joint_names", "transforms", "twist", "wrench")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    WRENCH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    transforms: _containers.RepeatedCompositeFieldContainer[_transform_pb2.Transform]
    twist: _containers.RepeatedCompositeFieldContainer[_twist_pb2.Twist]
    wrench: _containers.RepeatedCompositeFieldContainer[_wrench_pb2.Wrench]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., joint_names: _Optional[_Iterable[str]] = ..., transforms: _Optional[_Iterable[_Union[_transform_pb2.Transform, _Mapping]]] = ..., twist: _Optional[_Iterable[_Union[_twist_pb2.Twist, _Mapping]]] = ..., wrench: _Optional[_Iterable[_Union[_wrench_pb2.Wrench, _Mapping]]] = ...) -> None: ...
