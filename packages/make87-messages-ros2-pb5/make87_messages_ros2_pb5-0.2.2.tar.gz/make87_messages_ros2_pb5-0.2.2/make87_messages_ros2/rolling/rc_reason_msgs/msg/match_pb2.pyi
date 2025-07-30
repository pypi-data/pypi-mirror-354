from make87_messages_ros2.rolling.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Match(_message.Message):
    __slots__ = ("template_id", "uuid", "pose", "grasp_uuids", "score")
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    GRASP_UUIDS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    template_id: str
    uuid: str
    pose: _pose_stamped_pb2.PoseStamped
    grasp_uuids: _containers.RepeatedScalarFieldContainer[str]
    score: float
    def __init__(self, template_id: _Optional[str] = ..., uuid: _Optional[str] = ..., pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., grasp_uuids: _Optional[_Iterable[str]] = ..., score: _Optional[float] = ...) -> None: ...
