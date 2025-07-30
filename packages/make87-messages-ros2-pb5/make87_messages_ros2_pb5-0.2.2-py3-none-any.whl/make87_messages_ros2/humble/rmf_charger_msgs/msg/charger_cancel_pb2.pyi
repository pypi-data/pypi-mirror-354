from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargerCancel(_message.Message):
    __slots__ = ("header", "charger_name", "request_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHARGER_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    charger_name: str
    request_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., charger_name: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...
