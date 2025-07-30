from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CONmtIDRequest(_message.Message):
    __slots__ = ("header", "nmtcommand", "nodeid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NMTCOMMAND_FIELD_NUMBER: _ClassVar[int]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    nmtcommand: int
    nodeid: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., nmtcommand: _Optional[int] = ..., nodeid: _Optional[int] = ...) -> None: ...

class CONmtIDResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
