from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_with_covariance_stamped_pb2 as _pose_with_covariance_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetInitialPoseRequest(_message.Message):
    __slots__ = ("pose",)
    POSE_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped
    def __init__(self, pose: _Optional[_Union[_pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped, _Mapping]] = ...) -> None: ...

class SetInitialPoseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
