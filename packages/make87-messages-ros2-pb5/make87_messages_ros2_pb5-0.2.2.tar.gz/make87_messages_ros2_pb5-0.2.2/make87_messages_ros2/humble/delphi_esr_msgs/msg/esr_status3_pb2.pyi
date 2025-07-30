from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrStatus3(_message.Message):
    __slots__ = ("header", "ros2_header", "canmsg", "interface_version", "hw_version", "sw_version_host", "serial_num", "sw_version_pld")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_VERSION_FIELD_NUMBER: _ClassVar[int]
    HW_VERSION_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_HOST_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUM_FIELD_NUMBER: _ClassVar[int]
    SW_VERSION_PLD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    canmsg: str
    interface_version: int
    hw_version: int
    sw_version_host: str
    serial_num: str
    sw_version_pld: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., interface_version: _Optional[int] = ..., hw_version: _Optional[int] = ..., sw_version_host: _Optional[str] = ..., serial_num: _Optional[str] = ..., sw_version_pld: _Optional[int] = ...) -> None: ...
