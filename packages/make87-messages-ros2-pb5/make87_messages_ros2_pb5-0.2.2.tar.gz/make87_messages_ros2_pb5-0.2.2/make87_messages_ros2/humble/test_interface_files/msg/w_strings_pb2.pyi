from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WStrings(_message.Message):
    __slots__ = ("header", "wstring_value", "wstring_value_default1", "wstring_value_default2", "wstring_value_default3", "array_of_wstrings", "bounded_sequence_of_wstrings", "unbounded_sequence_of_wstrings")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WSTRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    WSTRING_VALUE_DEFAULT1_FIELD_NUMBER: _ClassVar[int]
    WSTRING_VALUE_DEFAULT2_FIELD_NUMBER: _ClassVar[int]
    WSTRING_VALUE_DEFAULT3_FIELD_NUMBER: _ClassVar[int]
    ARRAY_OF_WSTRINGS_FIELD_NUMBER: _ClassVar[int]
    BOUNDED_SEQUENCE_OF_WSTRINGS_FIELD_NUMBER: _ClassVar[int]
    UNBOUNDED_SEQUENCE_OF_WSTRINGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    wstring_value: str
    wstring_value_default1: str
    wstring_value_default2: str
    wstring_value_default3: str
    array_of_wstrings: _containers.RepeatedScalarFieldContainer[str]
    bounded_sequence_of_wstrings: _containers.RepeatedScalarFieldContainer[str]
    unbounded_sequence_of_wstrings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., wstring_value: _Optional[str] = ..., wstring_value_default1: _Optional[str] = ..., wstring_value_default2: _Optional[str] = ..., wstring_value_default3: _Optional[str] = ..., array_of_wstrings: _Optional[_Iterable[str]] = ..., bounded_sequence_of_wstrings: _Optional[_Iterable[str]] = ..., unbounded_sequence_of_wstrings: _Optional[_Iterable[str]] = ...) -> None: ...
