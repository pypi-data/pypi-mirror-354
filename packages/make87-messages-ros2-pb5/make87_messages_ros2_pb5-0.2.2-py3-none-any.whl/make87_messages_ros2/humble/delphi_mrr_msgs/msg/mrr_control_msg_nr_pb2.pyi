from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrControlMsgNR(_message.Message):
    __slots__ = ("header", "ros2_header", "can_stop_frequency_nrml", "can_prp_factor_nrml", "can_desired_sweep_bw_nrml", "can_radiation_ctrl", "can_stop_frequency_nrll", "can_prp_factor_nrll", "can_desired_sweep_bw_nrll")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_STOP_FREQUENCY_NRML_FIELD_NUMBER: _ClassVar[int]
    CAN_PRP_FACTOR_NRML_FIELD_NUMBER: _ClassVar[int]
    CAN_DESIRED_SWEEP_BW_NRML_FIELD_NUMBER: _ClassVar[int]
    CAN_RADIATION_CTRL_FIELD_NUMBER: _ClassVar[int]
    CAN_STOP_FREQUENCY_NRLL_FIELD_NUMBER: _ClassVar[int]
    CAN_PRP_FACTOR_NRLL_FIELD_NUMBER: _ClassVar[int]
    CAN_DESIRED_SWEEP_BW_NRLL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_stop_frequency_nrml: int
    can_prp_factor_nrml: int
    can_desired_sweep_bw_nrml: int
    can_radiation_ctrl: bool
    can_stop_frequency_nrll: int
    can_prp_factor_nrll: int
    can_desired_sweep_bw_nrll: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_stop_frequency_nrml: _Optional[int] = ..., can_prp_factor_nrml: _Optional[int] = ..., can_desired_sweep_bw_nrml: _Optional[int] = ..., can_radiation_ctrl: bool = ..., can_stop_frequency_nrll: _Optional[int] = ..., can_prp_factor_nrll: _Optional[int] = ..., can_desired_sweep_bw_nrll: _Optional[int] = ...) -> None: ...
