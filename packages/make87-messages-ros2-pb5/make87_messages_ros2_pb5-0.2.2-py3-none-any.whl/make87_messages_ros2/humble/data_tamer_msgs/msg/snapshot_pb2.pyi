from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Snapshot(_message.Message):
    __slots__ = ("header", "timestamp_nsec", "schema_hash", "active_mask", "payload")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_NSEC_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_HASH_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_MASK_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp_nsec: int
    schema_hash: int
    active_mask: _containers.RepeatedScalarFieldContainer[int]
    payload: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp_nsec: _Optional[int] = ..., schema_hash: _Optional[int] = ..., active_mask: _Optional[_Iterable[int]] = ..., payload: _Optional[_Iterable[int]] = ...) -> None: ...
