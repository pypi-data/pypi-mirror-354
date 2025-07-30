from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetEntityPoseRequest(_message.Message):
    __slots__ = ("entity", "pose")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    entity: _entity_pb2.Entity
    pose: _pose_pb2.Pose
    def __init__(self, entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class SetEntityPoseResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
