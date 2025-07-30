from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import route_path_pb2 as _route_path_pb2
from make87_messages_ros2.humble.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRoutePlanRequest(_message.Message):
    __slots__ = ("header", "network", "start", "goal")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    network: _uuid_pb2.UUID
    start: _uuid_pb2.UUID
    goal: _uuid_pb2.UUID
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., network: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., start: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., goal: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ...) -> None: ...

class GetRoutePlanResponse(_message.Message):
    __slots__ = ("header", "success", "status", "plan")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status: str
    plan: _route_path_pb2.RoutePath
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status: _Optional[str] = ..., plan: _Optional[_Union[_route_path_pb2.RoutePath, _Mapping]] = ...) -> None: ...
