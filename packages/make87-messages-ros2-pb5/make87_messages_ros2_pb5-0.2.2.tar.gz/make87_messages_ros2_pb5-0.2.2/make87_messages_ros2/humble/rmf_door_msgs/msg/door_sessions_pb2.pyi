from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_door_msgs.msg import session_pb2 as _session_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DoorSessions(_message.Message):
    __slots__ = ("header", "door_name", "sessions")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DOOR_NAME_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    door_name: str
    sessions: _containers.RepeatedCompositeFieldContainer[_session_pb2.Session]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., door_name: _Optional[str] = ..., sessions: _Optional[_Iterable[_Union[_session_pb2.Session, _Mapping]]] = ...) -> None: ...
