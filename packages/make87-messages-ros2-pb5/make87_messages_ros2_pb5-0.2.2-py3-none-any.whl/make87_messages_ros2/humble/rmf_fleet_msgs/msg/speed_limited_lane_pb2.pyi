from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpeedLimitedLane(_message.Message):
    __slots__ = ("header", "lane_index", "speed_limit")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lane_index: int
    speed_limit: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lane_index: _Optional[int] = ..., speed_limit: _Optional[float] = ...) -> None: ...
