from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import nav_satsv_pb2 as _nav_satsv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSAT(_message.Message):
    __slots__ = ("header", "i_tow", "version", "num_svs", "reserved0", "sv")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SVS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    version: int
    num_svs: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    sv: _containers.RepeatedCompositeFieldContainer[_nav_satsv_pb2.NavSATSV]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., version: _Optional[int] = ..., num_svs: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., sv: _Optional[_Iterable[_Union[_nav_satsv_pb2.NavSATSV, _Mapping]]] = ...) -> None: ...
