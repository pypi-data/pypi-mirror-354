from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccContainerInitialStatusCmd(_message.Message):
    __slots__ = ("header", "path", "initial_states", "local_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: str
    initial_states: _containers.RepeatedScalarFieldContainer[str]
    local_data: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[str] = ..., initial_states: _Optional[_Iterable[str]] = ..., local_data: _Optional[str] = ...) -> None: ...
