from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import cor_status_info_pb2 as _cor_status_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXRxmCor(_message.Message):
    __slots__ = ("header", "ros2_header", "version", "ebno", "status_info", "msg_type", "msg_sub_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    EBNO_FIELD_NUMBER: _ClassVar[int]
    STATUS_INFO_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    version: int
    ebno: int
    status_info: _cor_status_info_pb2.CorStatusInfo
    msg_type: int
    msg_sub_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., version: _Optional[int] = ..., ebno: _Optional[int] = ..., status_info: _Optional[_Union[_cor_status_info_pb2.CorStatusInfo, _Mapping]] = ..., msg_type: _Optional[int] = ..., msg_sub_type: _Optional[int] = ...) -> None: ...
