from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PathPoint(_message.Message):
    __slots__ = ("header", "pose", "longitudinal_velocity_mps", "lateral_velocity_mps", "heading_rate_rps", "is_final")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_VELOCITY_MPS_FIELD_NUMBER: _ClassVar[int]
    LATERAL_VELOCITY_MPS_FIELD_NUMBER: _ClassVar[int]
    HEADING_RATE_RPS_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose: _pose_pb2.Pose
    longitudinal_velocity_mps: float
    lateral_velocity_mps: float
    heading_rate_rps: float
    is_final: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., longitudinal_velocity_mps: _Optional[float] = ..., lateral_velocity_mps: _Optional[float] = ..., heading_rate_rps: _Optional[float] = ..., is_final: bool = ...) -> None: ...
