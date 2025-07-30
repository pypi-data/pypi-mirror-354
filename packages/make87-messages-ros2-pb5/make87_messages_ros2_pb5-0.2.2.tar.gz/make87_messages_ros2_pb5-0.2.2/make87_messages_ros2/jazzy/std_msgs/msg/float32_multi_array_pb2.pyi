from make87_messages_ros2.jazzy.std_msgs.msg import multi_array_layout_pb2 as _multi_array_layout_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Float32MultiArray(_message.Message):
    __slots__ = ("layout", "data")
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    layout: _multi_array_layout_pb2.MultiArrayLayout
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, layout: _Optional[_Union[_multi_array_layout_pb2.MultiArrayLayout, _Mapping]] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...
