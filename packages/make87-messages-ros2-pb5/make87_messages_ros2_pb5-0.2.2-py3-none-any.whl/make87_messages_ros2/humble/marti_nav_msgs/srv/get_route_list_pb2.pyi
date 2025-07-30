from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_nav_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRouteListRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetRouteListResponse(_message.Message):
    __slots__ = ("header", "routes", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    routes: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., routes: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
