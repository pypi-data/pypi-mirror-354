from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraGetExposureModeEVRequest(_message.Message):
    __slots__ = ("header", "payload_index")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ...) -> None: ...

class CameraGetExposureModeEVResponse(_message.Message):
    __slots__ = ("header", "success", "exposure_mode", "ev_factor")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_MODE_FIELD_NUMBER: _ClassVar[int]
    EV_FACTOR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    exposure_mode: int
    ev_factor: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., exposure_mode: _Optional[int] = ..., ev_factor: _Optional[int] = ...) -> None: ...
