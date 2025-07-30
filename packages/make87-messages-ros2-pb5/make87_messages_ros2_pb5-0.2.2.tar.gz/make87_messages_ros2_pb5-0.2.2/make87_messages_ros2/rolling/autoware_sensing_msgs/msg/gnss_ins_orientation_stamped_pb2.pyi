from make87_messages_ros2.rolling.autoware_sensing_msgs.msg import gnss_ins_orientation_pb2 as _gnss_ins_orientation_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GnssInsOrientationStamped(_message.Message):
    __slots__ = ("header", "orientation")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orientation: _gnss_ins_orientation_pb2.GnssInsOrientation
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orientation: _Optional[_Union[_gnss_ins_orientation_pb2.GnssInsOrientation, _Mapping]] = ...) -> None: ...
