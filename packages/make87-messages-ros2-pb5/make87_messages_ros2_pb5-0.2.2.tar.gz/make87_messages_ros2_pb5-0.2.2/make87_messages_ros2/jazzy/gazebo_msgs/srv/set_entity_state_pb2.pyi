from make87_messages_ros2.jazzy.gazebo_msgs.msg import entity_state_pb2 as _entity_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetEntityStateRequest(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: _entity_state_pb2.EntityState
    def __init__(self, state: _Optional[_Union[_entity_state_pb2.EntityState, _Mapping]] = ...) -> None: ...

class SetEntityStateResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
