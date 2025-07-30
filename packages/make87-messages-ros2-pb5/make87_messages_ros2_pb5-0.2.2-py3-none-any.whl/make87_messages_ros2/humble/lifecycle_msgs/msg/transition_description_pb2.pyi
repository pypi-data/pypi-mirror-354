from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import state_pb2 as _state_pb2
from make87_messages_ros2.humble.lifecycle_msgs.msg import transition_pb2 as _transition_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransitionDescription(_message.Message):
    __slots__ = ("header", "transition", "start_state", "goal_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    GOAL_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    transition: _transition_pb2.Transition
    start_state: _state_pb2.State
    goal_state: _state_pb2.State
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., transition: _Optional[_Union[_transition_pb2.Transition, _Mapping]] = ..., start_state: _Optional[_Union[_state_pb2.State, _Mapping]] = ..., goal_state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...
