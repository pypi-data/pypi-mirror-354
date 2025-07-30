from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ahbc(_message.Message):
    __slots__ = ("header", "ros2_header", "high_low_beam_decision", "reasons_for_switch_to_low_beam")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HIGH_LOW_BEAM_DECISION_FIELD_NUMBER: _ClassVar[int]
    REASONS_FOR_SWITCH_TO_LOW_BEAM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    high_low_beam_decision: int
    reasons_for_switch_to_low_beam: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., high_low_beam_decision: _Optional[int] = ..., reasons_for_switch_to_low_beam: _Optional[int] = ...) -> None: ...
