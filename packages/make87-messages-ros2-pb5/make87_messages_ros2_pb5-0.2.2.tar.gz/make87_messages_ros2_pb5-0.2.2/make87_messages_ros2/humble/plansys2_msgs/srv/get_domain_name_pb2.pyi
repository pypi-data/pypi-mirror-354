from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainNameRequest(_message.Message):
    __slots__ = ("header", "request")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request: _empty_pb2.Empty
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class GetDomainNameResponse(_message.Message):
    __slots__ = ("header", "success", "name", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    name: str
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., name: _Optional[str] = ..., error_info: _Optional[str] = ...) -> None: ...
