from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.smacc2_msgs.msg import smacc_event_pb2 as _smacc_event_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccStateReactor(_message.Message):
    __slots__ = ("header", "index", "type_name", "object_tag", "event_sources")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TAG_FIELD_NUMBER: _ClassVar[int]
    EVENT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    index: int
    type_name: str
    object_tag: str
    event_sources: _containers.RepeatedCompositeFieldContainer[_smacc_event_pb2.SmaccEvent]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., index: _Optional[int] = ..., type_name: _Optional[str] = ..., object_tag: _Optional[str] = ..., event_sources: _Optional[_Iterable[_Union[_smacc_event_pb2.SmaccEvent, _Mapping]]] = ...) -> None: ...
