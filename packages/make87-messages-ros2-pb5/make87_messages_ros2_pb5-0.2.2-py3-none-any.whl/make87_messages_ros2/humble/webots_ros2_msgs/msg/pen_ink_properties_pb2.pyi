from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PenInkProperties(_message.Message):
    __slots__ = ("header", "color", "density")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DENSITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    color: int
    density: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., color: _Optional[int] = ..., density: _Optional[float] = ...) -> None: ...
