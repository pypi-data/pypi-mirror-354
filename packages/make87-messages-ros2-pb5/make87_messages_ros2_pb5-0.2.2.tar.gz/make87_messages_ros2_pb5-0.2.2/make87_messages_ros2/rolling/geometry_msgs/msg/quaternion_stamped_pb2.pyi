from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaternionStamped(_message.Message):
    __slots__ = ("header", "quaternion")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUATERNION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    quaternion: _quaternion_pb2.Quaternion
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., quaternion: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ...) -> None: ...
