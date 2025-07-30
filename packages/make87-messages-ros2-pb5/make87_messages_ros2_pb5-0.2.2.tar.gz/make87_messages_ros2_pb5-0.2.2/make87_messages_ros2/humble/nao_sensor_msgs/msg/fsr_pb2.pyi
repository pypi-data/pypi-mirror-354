from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FSR(_message.Message):
    __slots__ = ("header", "l_foot_front_left", "l_foot_front_right", "l_foot_back_left", "l_foot_back_right", "r_foot_front_left", "r_foot_front_right", "r_foot_back_left", "r_foot_back_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BACK_LEFT_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BACK_RIGHT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BACK_LEFT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BACK_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    l_foot_front_left: float
    l_foot_front_right: float
    l_foot_back_left: float
    l_foot_back_right: float
    r_foot_front_left: float
    r_foot_front_right: float
    r_foot_back_left: float
    r_foot_back_right: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., l_foot_front_left: _Optional[float] = ..., l_foot_front_right: _Optional[float] = ..., l_foot_back_left: _Optional[float] = ..., l_foot_back_right: _Optional[float] = ..., r_foot_front_left: _Optional[float] = ..., r_foot_front_right: _Optional[float] = ..., r_foot_back_left: _Optional[float] = ..., r_foot_back_right: _Optional[float] = ...) -> None: ...
