from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Extrinsics(_message.Message):
    __slots__ = ("rotation", "translation")
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    rotation: _containers.RepeatedScalarFieldContainer[float]
    translation: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, rotation: _Optional[_Iterable[float]] = ..., translation: _Optional[_Iterable[float]] = ...) -> None: ...
