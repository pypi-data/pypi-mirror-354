from make87_messages_ros2.jazzy.rosapi_msgs.msg import type_def_pb2 as _type_def_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageDetailsRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class MessageDetailsResponse(_message.Message):
    __slots__ = ("typedefs",)
    TYPEDEFS_FIELD_NUMBER: _ClassVar[int]
    typedefs: _containers.RepeatedCompositeFieldContainer[_type_def_pb2.TypeDef]
    def __init__(self, typedefs: _Optional[_Iterable[_Union[_type_def_pb2.TypeDef, _Mapping]]] = ...) -> None: ...
