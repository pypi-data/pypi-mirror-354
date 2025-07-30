from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleIdentity(_message.Message):
    __slots__ = ("node_uuid", "timestamp")
    NODE_UUID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    node_uuid: str
    timestamp: _time_pb2.Time
    def __init__(self, node_uuid: _Optional[str] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
