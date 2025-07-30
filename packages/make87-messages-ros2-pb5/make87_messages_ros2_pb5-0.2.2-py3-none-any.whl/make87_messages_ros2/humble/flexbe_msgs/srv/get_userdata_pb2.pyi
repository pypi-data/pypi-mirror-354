from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.flexbe_msgs.msg import userdata_info_pb2 as _userdata_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserdataRequest(_message.Message):
    __slots__ = ("header", "userdata_key")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    USERDATA_KEY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    userdata_key: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., userdata_key: _Optional[str] = ...) -> None: ...

class GetUserdataResponse(_message.Message):
    __slots__ = ("header", "success", "message", "userdata")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    userdata: _containers.RepeatedCompositeFieldContainer[_userdata_info_pb2.UserdataInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ..., userdata: _Optional[_Iterable[_Union[_userdata_info_pb2.UserdataInfo, _Mapping]]] = ...) -> None: ...
