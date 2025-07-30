from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AhbcGradual(_message.Message):
    __slots__ = ("header", "ros2_header", "boundary_domain_bottom_non_glare_hlb", "boundary_domain_non_glare_left_hand_hlb", "boundary_domain_non_glare_right_hand_hlb", "object_distance_hlb", "status_boundary_domain_bottom_non_glare_hlb", "status_boundary_domain_non_glare_left_hand_hlb", "status_boundary_domain_non_glare_right_hand_hlb", "status_object_distance_hlb", "left_target_change", "right_target_change", "too_many_cars", "busy_scene")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_DOMAIN_BOTTOM_NON_GLARE_HLB_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_DOMAIN_NON_GLARE_LEFT_HAND_HLB_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_DOMAIN_NON_GLARE_RIGHT_HAND_HLB_FIELD_NUMBER: _ClassVar[int]
    OBJECT_DISTANCE_HLB_FIELD_NUMBER: _ClassVar[int]
    STATUS_BOUNDARY_DOMAIN_BOTTOM_NON_GLARE_HLB_FIELD_NUMBER: _ClassVar[int]
    STATUS_BOUNDARY_DOMAIN_NON_GLARE_LEFT_HAND_HLB_FIELD_NUMBER: _ClassVar[int]
    STATUS_BOUNDARY_DOMAIN_NON_GLARE_RIGHT_HAND_HLB_FIELD_NUMBER: _ClassVar[int]
    STATUS_OBJECT_DISTANCE_HLB_FIELD_NUMBER: _ClassVar[int]
    LEFT_TARGET_CHANGE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TARGET_CHANGE_FIELD_NUMBER: _ClassVar[int]
    TOO_MANY_CARS_FIELD_NUMBER: _ClassVar[int]
    BUSY_SCENE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    boundary_domain_bottom_non_glare_hlb: float
    boundary_domain_non_glare_left_hand_hlb: float
    boundary_domain_non_glare_right_hand_hlb: float
    object_distance_hlb: int
    status_boundary_domain_bottom_non_glare_hlb: int
    status_boundary_domain_non_glare_left_hand_hlb: int
    status_boundary_domain_non_glare_right_hand_hlb: int
    status_object_distance_hlb: int
    left_target_change: bool
    right_target_change: bool
    too_many_cars: bool
    busy_scene: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., boundary_domain_bottom_non_glare_hlb: _Optional[float] = ..., boundary_domain_non_glare_left_hand_hlb: _Optional[float] = ..., boundary_domain_non_glare_right_hand_hlb: _Optional[float] = ..., object_distance_hlb: _Optional[int] = ..., status_boundary_domain_bottom_non_glare_hlb: _Optional[int] = ..., status_boundary_domain_non_glare_left_hand_hlb: _Optional[int] = ..., status_boundary_domain_non_glare_right_hand_hlb: _Optional[int] = ..., status_object_distance_hlb: _Optional[int] = ..., left_target_change: bool = ..., right_target_change: bool = ..., too_many_cars: bool = ..., busy_scene: bool = ...) -> None: ...
