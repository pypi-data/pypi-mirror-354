from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReassignCommandIdCmd(_message.Message):
    __slots__ = ("header", "ros2_header", "confirm", "command_id_index", "user_command_id", "disable_default_command_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ID_INDEX_FIELD_NUMBER: _ClassVar[int]
    USER_COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DEFAULT_COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    confirm: bool
    command_id_index: int
    user_command_id: int
    disable_default_command_id: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., confirm: bool = ..., command_id_index: _Optional[int] = ..., user_command_id: _Optional[int] = ..., disable_default_command_id: bool = ...) -> None: ...
