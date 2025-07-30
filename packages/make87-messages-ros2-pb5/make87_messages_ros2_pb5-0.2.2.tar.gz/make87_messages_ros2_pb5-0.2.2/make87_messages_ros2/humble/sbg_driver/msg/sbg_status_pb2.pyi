from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_status_aiding_pb2 as _sbg_status_aiding_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_status_com_pb2 as _sbg_status_com_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_status_general_pb2 as _sbg_status_general_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "status_general", "status_com", "status_aiding")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_GENERAL_FIELD_NUMBER: _ClassVar[int]
    STATUS_COM_FIELD_NUMBER: _ClassVar[int]
    STATUS_AIDING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    status_general: _sbg_status_general_pb2.SbgStatusGeneral
    status_com: _sbg_status_com_pb2.SbgStatusCom
    status_aiding: _sbg_status_aiding_pb2.SbgStatusAiding
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., status_general: _Optional[_Union[_sbg_status_general_pb2.SbgStatusGeneral, _Mapping]] = ..., status_com: _Optional[_Union[_sbg_status_com_pb2.SbgStatusCom, _Mapping]] = ..., status_aiding: _Optional[_Union[_sbg_status_aiding_pb2.SbgStatusAiding, _Mapping]] = ...) -> None: ...
