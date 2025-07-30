from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetMavFrameRequest(_message.Message):
    __slots__ = ("header", "mav_frame")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAV_FRAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mav_frame: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mav_frame: _Optional[int] = ...) -> None: ...

class SetMavFrameResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
