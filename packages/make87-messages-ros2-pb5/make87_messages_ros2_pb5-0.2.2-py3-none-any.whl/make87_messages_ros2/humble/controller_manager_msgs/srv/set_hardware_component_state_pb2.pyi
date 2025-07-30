from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetHardwareComponentStateRequest(_message.Message):
    __slots__ = ("header", "name", "target_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    target_state: _state_pb2.State
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., target_state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...

class SetHardwareComponentStateResponse(_message.Message):
    __slots__ = ("header", "ok", "state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ok: bool
    state: _state_pb2.State
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ok: bool = ..., state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...
