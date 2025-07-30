from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inertia(_message.Message):
    __slots__ = ("header", "m", "com", "ixx", "ixy", "ixz", "iyy", "iyz", "izz")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    COM_FIELD_NUMBER: _ClassVar[int]
    IXX_FIELD_NUMBER: _ClassVar[int]
    IXY_FIELD_NUMBER: _ClassVar[int]
    IXZ_FIELD_NUMBER: _ClassVar[int]
    IYY_FIELD_NUMBER: _ClassVar[int]
    IYZ_FIELD_NUMBER: _ClassVar[int]
    IZZ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    m: float
    com: _vector3_pb2.Vector3
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., m: _Optional[float] = ..., com: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., ixx: _Optional[float] = ..., ixy: _Optional[float] = ..., ixz: _Optional[float] = ..., iyy: _Optional[float] = ..., iyz: _Optional[float] = ..., izz: _Optional[float] = ...) -> None: ...
