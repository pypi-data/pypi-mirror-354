from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalDeviceSetAttitude(_message.Message):
    __slots__ = ("target_system", "target_component", "flags", "q", "angular_velocity_x", "angular_velocity_y", "angular_velocity_z")
    TARGET_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TARGET_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_Z_FIELD_NUMBER: _ClassVar[int]
    target_system: int
    target_component: int
    flags: int
    q: _quaternion_pb2.Quaternion
    angular_velocity_x: float
    angular_velocity_y: float
    angular_velocity_z: float
    def __init__(self, target_system: _Optional[int] = ..., target_component: _Optional[int] = ..., flags: _Optional[int] = ..., q: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., angular_velocity_x: _Optional[float] = ..., angular_velocity_y: _Optional[float] = ..., angular_velocity_z: _Optional[float] = ...) -> None: ...
