from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanPoint(_message.Message):
    __slots__ = ("header", "angle", "distance", "reflectivity", "valid", "infinite", "glare", "reflector", "contamination", "contamination_warning")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REFLECTIVITY_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    INFINITE_FIELD_NUMBER: _ClassVar[int]
    GLARE_FIELD_NUMBER: _ClassVar[int]
    REFLECTOR_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_WARNING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    angle: float
    distance: int
    reflectivity: int
    valid: bool
    infinite: bool
    glare: bool
    reflector: bool
    contamination: bool
    contamination_warning: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., angle: _Optional[float] = ..., distance: _Optional[int] = ..., reflectivity: _Optional[int] = ..., valid: bool = ..., infinite: bool = ..., glare: bool = ..., reflector: bool = ..., contamination: bool = ..., contamination_warning: bool = ...) -> None: ...
