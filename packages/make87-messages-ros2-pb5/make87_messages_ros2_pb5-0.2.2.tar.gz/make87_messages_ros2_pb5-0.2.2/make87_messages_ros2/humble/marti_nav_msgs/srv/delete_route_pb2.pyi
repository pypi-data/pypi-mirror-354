from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteRouteRequest(_message.Message):
    __slots__ = ("header", "guid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GUID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    guid: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., guid: _Optional[str] = ...) -> None: ...

class DeleteRouteResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
