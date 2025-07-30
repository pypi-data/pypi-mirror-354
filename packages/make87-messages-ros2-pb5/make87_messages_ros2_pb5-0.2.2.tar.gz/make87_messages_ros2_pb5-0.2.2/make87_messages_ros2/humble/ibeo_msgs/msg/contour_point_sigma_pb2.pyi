from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContourPointSigma(_message.Message):
    __slots__ = ("header", "x", "y", "x_sigma", "y_sigma")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    X_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Y_SIGMA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x: int
    y: int
    x_sigma: int
    y_sigma: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., x_sigma: _Optional[int] = ..., y_sigma: _Optional[int] = ...) -> None: ...
