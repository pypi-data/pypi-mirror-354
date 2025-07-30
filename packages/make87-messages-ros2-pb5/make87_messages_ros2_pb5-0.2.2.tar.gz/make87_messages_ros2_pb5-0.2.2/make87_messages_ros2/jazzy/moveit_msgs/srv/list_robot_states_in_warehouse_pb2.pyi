from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListRobotStatesInWarehouseRequest(_message.Message):
    __slots__ = ("regex", "robot")
    REGEX_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    regex: str
    robot: str
    def __init__(self, regex: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class ListRobotStatesInWarehouseResponse(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, states: _Optional[_Iterable[str]] = ...) -> None: ...
