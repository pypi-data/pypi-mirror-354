from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MountConfigureRequest(_message.Message):
    __slots__ = ("header", "ros2_header", "mode", "stabilize_roll", "stabilize_pitch", "stabilize_yaw", "roll_input", "pitch_input", "yaw_input")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    STABILIZE_ROLL_FIELD_NUMBER: _ClassVar[int]
    STABILIZE_PITCH_FIELD_NUMBER: _ClassVar[int]
    STABILIZE_YAW_FIELD_NUMBER: _ClassVar[int]
    ROLL_INPUT_FIELD_NUMBER: _ClassVar[int]
    PITCH_INPUT_FIELD_NUMBER: _ClassVar[int]
    YAW_INPUT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    mode: int
    stabilize_roll: bool
    stabilize_pitch: bool
    stabilize_yaw: bool
    roll_input: int
    pitch_input: int
    yaw_input: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., mode: _Optional[int] = ..., stabilize_roll: bool = ..., stabilize_pitch: bool = ..., stabilize_yaw: bool = ..., roll_input: _Optional[int] = ..., pitch_input: _Optional[int] = ..., yaw_input: _Optional[int] = ...) -> None: ...

class MountConfigureResponse(_message.Message):
    __slots__ = ("header", "success", "result")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
