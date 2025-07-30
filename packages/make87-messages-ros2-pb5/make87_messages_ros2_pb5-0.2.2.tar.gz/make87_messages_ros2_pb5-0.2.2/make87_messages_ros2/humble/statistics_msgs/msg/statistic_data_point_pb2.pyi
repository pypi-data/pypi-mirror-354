from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatisticDataPoint(_message.Message):
    __slots__ = ("header", "data_type", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data_type: int
    data: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data_type: _Optional[int] = ..., data: _Optional[float] = ...) -> None: ...
