from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrStatusCanVersion(_message.Message):
    __slots__ = ("header", "ros2_header", "can_usc_section_compatibility", "can_pcan_minor_mrr", "can_pcan_major_mrr")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_USC_SECTION_COMPATIBILITY_FIELD_NUMBER: _ClassVar[int]
    CAN_PCAN_MINOR_MRR_FIELD_NUMBER: _ClassVar[int]
    CAN_PCAN_MAJOR_MRR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_usc_section_compatibility: int
    can_pcan_minor_mrr: int
    can_pcan_major_mrr: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_usc_section_compatibility: _Optional[int] = ..., can_pcan_minor_mrr: _Optional[int] = ..., can_pcan_major_mrr: _Optional[int] = ...) -> None: ...
