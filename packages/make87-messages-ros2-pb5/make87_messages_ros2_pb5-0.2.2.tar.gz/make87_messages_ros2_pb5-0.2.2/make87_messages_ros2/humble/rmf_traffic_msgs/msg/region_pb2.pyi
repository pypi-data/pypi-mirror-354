from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import space_pb2 as _space_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import timespan_pb2 as _timespan_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Region(_message.Message):
    __slots__ = ("header", "map", "spaces", "timespan")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    SPACES_FIELD_NUMBER: _ClassVar[int]
    TIMESPAN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: str
    spaces: _containers.RepeatedCompositeFieldContainer[_space_pb2.Space]
    timespan: _timespan_pb2.Timespan
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[str] = ..., spaces: _Optional[_Iterable[_Union[_space_pb2.Space, _Mapping]]] = ..., timespan: _Optional[_Union[_timespan_pb2.Timespan, _Mapping]] = ...) -> None: ...
