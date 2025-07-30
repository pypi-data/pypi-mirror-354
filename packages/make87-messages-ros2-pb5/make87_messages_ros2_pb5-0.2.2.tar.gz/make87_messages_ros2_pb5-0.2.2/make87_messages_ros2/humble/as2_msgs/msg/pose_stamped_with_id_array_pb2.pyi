from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import pose_stamped_with_id_pb2 as _pose_stamped_with_id_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PoseStampedWithIDArray(_message.Message):
    __slots__ = ("header", "poses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    poses: _containers.RepeatedCompositeFieldContainer[_pose_stamped_with_id_pb2.PoseStampedWithID]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., poses: _Optional[_Iterable[_Union[_pose_stamped_with_id_pb2.PoseStampedWithID, _Mapping]]] = ...) -> None: ...
