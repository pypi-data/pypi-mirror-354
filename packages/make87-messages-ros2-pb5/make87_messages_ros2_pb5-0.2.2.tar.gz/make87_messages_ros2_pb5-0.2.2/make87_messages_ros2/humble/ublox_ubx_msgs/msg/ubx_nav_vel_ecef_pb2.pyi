from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavVelECEF(_message.Message):
    __slots__ = ("header", "ros2_header", "itow", "ecef_vx", "ecef_vy", "ecef_vz", "s_acc")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_VX_FIELD_NUMBER: _ClassVar[int]
    ECEF_VY_FIELD_NUMBER: _ClassVar[int]
    ECEF_VZ_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    itow: int
    ecef_vx: int
    ecef_vy: int
    ecef_vz: int
    s_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., itow: _Optional[int] = ..., ecef_vx: _Optional[int] = ..., ecef_vy: _Optional[int] = ..., ecef_vz: _Optional[int] = ..., s_acc: _Optional[int] = ...) -> None: ...
