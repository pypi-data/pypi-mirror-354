from make87_messages_ros2.rolling.moveit_msgs.msg import motion_sequence_item_pb2 as _motion_sequence_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MotionSequenceRequest(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_motion_sequence_item_pb2.MotionSequenceItem]
    def __init__(self, items: _Optional[_Iterable[_Union[_motion_sequence_item_pb2.MotionSequenceItem, _Mapping]]] = ...) -> None: ...
