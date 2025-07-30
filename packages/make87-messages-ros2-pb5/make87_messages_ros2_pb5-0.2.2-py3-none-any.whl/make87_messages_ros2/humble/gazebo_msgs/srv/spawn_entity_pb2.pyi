from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpawnEntityRequest(_message.Message):
    __slots__ = ("header", "name", "xml", "robot_namespace", "initial_pose", "reference_frame")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    XML_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    xml: str
    robot_namespace: str
    initial_pose: _pose_pb2.Pose
    reference_frame: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., xml: _Optional[str] = ..., robot_namespace: _Optional[str] = ..., initial_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., reference_frame: _Optional[str] = ...) -> None: ...

class SpawnEntityResponse(_message.Message):
    __slots__ = ("header", "success", "status_message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
