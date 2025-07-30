from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelRxStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "novatel_msg_header", "error", "rxstat", "aux1stat", "aux2stat", "aux3stat", "aux4stat")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RXSTAT_FIELD_NUMBER: _ClassVar[int]
    AUX1STAT_FIELD_NUMBER: _ClassVar[int]
    AUX2STAT_FIELD_NUMBER: _ClassVar[int]
    AUX3STAT_FIELD_NUMBER: _ClassVar[int]
    AUX4STAT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    error: int
    rxstat: int
    aux1stat: int
    aux2stat: int
    aux3stat: int
    aux4stat: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., error: _Optional[int] = ..., rxstat: _Optional[int] = ..., aux1stat: _Optional[int] = ..., aux2stat: _Optional[int] = ..., aux3stat: _Optional[int] = ..., aux4stat: _Optional[int] = ...) -> None: ...
