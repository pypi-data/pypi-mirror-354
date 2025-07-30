from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TsrVisionOnly(_message.Message):
    __slots__ = ("header", "ros2_header", "vision_only_sign_type_display1", "vision_only_supplementary_sign_type_display1", "vision_only_sign_type_display2", "vision_only_supplementary_sign_type_display2", "vision_only_sign_type_display3", "vision_only_supplementary_sign_type_display3", "vision_only_sign_type_display4", "vision_only_supplementary_sign_type_display4")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SIGN_TYPE_DISPLAY1_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SUPPLEMENTARY_SIGN_TYPE_DISPLAY1_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SIGN_TYPE_DISPLAY2_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SUPPLEMENTARY_SIGN_TYPE_DISPLAY2_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SIGN_TYPE_DISPLAY3_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SUPPLEMENTARY_SIGN_TYPE_DISPLAY3_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SIGN_TYPE_DISPLAY4_FIELD_NUMBER: _ClassVar[int]
    VISION_ONLY_SUPPLEMENTARY_SIGN_TYPE_DISPLAY4_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    vision_only_sign_type_display1: int
    vision_only_supplementary_sign_type_display1: int
    vision_only_sign_type_display2: int
    vision_only_supplementary_sign_type_display2: int
    vision_only_sign_type_display3: int
    vision_only_supplementary_sign_type_display3: int
    vision_only_sign_type_display4: int
    vision_only_supplementary_sign_type_display4: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., vision_only_sign_type_display1: _Optional[int] = ..., vision_only_supplementary_sign_type_display1: _Optional[int] = ..., vision_only_sign_type_display2: _Optional[int] = ..., vision_only_supplementary_sign_type_display2: _Optional[int] = ..., vision_only_sign_type_display3: _Optional[int] = ..., vision_only_supplementary_sign_type_display3: _Optional[int] = ..., vision_only_sign_type_display4: _Optional[int] = ..., vision_only_supplementary_sign_type_display4: _Optional[int] = ...) -> None: ...
