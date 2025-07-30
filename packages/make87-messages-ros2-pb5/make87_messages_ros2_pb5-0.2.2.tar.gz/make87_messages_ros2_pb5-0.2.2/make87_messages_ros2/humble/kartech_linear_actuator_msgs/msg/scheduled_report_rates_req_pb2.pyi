from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.kartech_linear_actuator_msgs.msg import report_index_pb2 as _report_index_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduledReportRatesReq(_message.Message):
    __slots__ = ("header", "ros2_header", "confirm", "index_1", "index_1_report_time", "index_2", "index_2_report_time")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    INDEX_1_FIELD_NUMBER: _ClassVar[int]
    INDEX_1_REPORT_TIME_FIELD_NUMBER: _ClassVar[int]
    INDEX_2_FIELD_NUMBER: _ClassVar[int]
    INDEX_2_REPORT_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    confirm: bool
    index_1: _report_index_pb2.ReportIndex
    index_1_report_time: int
    index_2: _report_index_pb2.ReportIndex
    index_2_report_time: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., confirm: bool = ..., index_1: _Optional[_Union[_report_index_pb2.ReportIndex, _Mapping]] = ..., index_1_report_time: _Optional[int] = ..., index_2: _Optional[_Union[_report_index_pb2.ReportIndex, _Mapping]] = ..., index_2_report_time: _Optional[int] = ...) -> None: ...
