from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class COReadRequest(_message.Message):
    __slots__ = ("header", "index", "subindex")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    index: int
    subindex: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., index: _Optional[int] = ..., subindex: _Optional[int] = ...) -> None: ...

class COReadResponse(_message.Message):
    __slots__ = ("header", "success", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    data: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., data: _Optional[int] = ...) -> None: ...
