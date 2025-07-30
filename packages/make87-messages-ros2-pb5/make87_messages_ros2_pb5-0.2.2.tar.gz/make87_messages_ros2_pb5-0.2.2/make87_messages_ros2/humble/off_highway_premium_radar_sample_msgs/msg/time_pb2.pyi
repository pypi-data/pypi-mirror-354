from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Time(_message.Message):
    __slots__ = ("header", "sec", "nanosec")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    NANOSEC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sec: int
    nanosec: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sec: _Optional[int] = ..., nanosec: _Optional[int] = ...) -> None: ...
