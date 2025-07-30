from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnsParasetToEEPROM(_message.Message):
    __slots__ = ("header", "ros2_header", "command", "paraset_cksum_low_byte", "paraset_cksum_high_byte")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    PARASET_CKSUM_LOW_BYTE_FIELD_NUMBER: _ClassVar[int]
    PARASET_CKSUM_HIGH_BYTE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    command: int
    paraset_cksum_low_byte: int
    paraset_cksum_high_byte: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., command: _Optional[int] = ..., paraset_cksum_low_byte: _Optional[int] = ..., paraset_cksum_high_byte: _Optional[int] = ...) -> None: ...
