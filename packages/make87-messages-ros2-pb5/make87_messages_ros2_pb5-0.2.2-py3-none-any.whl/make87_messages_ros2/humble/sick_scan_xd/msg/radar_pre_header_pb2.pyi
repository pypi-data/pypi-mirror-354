from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_scan_xd.msg import radar_pre_header_device_block_pb2 as _radar_pre_header_device_block_pb2
from make87_messages_ros2.humble.sick_scan_xd.msg import radar_pre_header_encoder_block_pb2 as _radar_pre_header_encoder_block_pb2
from make87_messages_ros2.humble.sick_scan_xd.msg import radar_pre_header_measurement_param1_block_pb2 as _radar_pre_header_measurement_param1_block_pb2
from make87_messages_ros2.humble.sick_scan_xd.msg import radar_pre_header_status_block_pb2 as _radar_pre_header_status_block_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeader(_message.Message):
    __slots__ = ("header", "uiversionno", "radarpreheaderdeviceblock", "radarpreheaderstatusblock", "radarpreheadermeasurementparam1block", "radarpreheaderarrayencoderblock")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UIVERSIONNO_FIELD_NUMBER: _ClassVar[int]
    RADARPREHEADERDEVICEBLOCK_FIELD_NUMBER: _ClassVar[int]
    RADARPREHEADERSTATUSBLOCK_FIELD_NUMBER: _ClassVar[int]
    RADARPREHEADERMEASUREMENTPARAM1BLOCK_FIELD_NUMBER: _ClassVar[int]
    RADARPREHEADERARRAYENCODERBLOCK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    uiversionno: int
    radarpreheaderdeviceblock: _radar_pre_header_device_block_pb2.RadarPreHeaderDeviceBlock
    radarpreheaderstatusblock: _radar_pre_header_status_block_pb2.RadarPreHeaderStatusBlock
    radarpreheadermeasurementparam1block: _radar_pre_header_measurement_param1_block_pb2.RadarPreHeaderMeasurementParam1Block
    radarpreheaderarrayencoderblock: _containers.RepeatedCompositeFieldContainer[_radar_pre_header_encoder_block_pb2.RadarPreHeaderEncoderBlock]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., uiversionno: _Optional[int] = ..., radarpreheaderdeviceblock: _Optional[_Union[_radar_pre_header_device_block_pb2.RadarPreHeaderDeviceBlock, _Mapping]] = ..., radarpreheaderstatusblock: _Optional[_Union[_radar_pre_header_status_block_pb2.RadarPreHeaderStatusBlock, _Mapping]] = ..., radarpreheadermeasurementparam1block: _Optional[_Union[_radar_pre_header_measurement_param1_block_pb2.RadarPreHeaderMeasurementParam1Block, _Mapping]] = ..., radarpreheaderarrayencoderblock: _Optional[_Iterable[_Union[_radar_pre_header_encoder_block_pb2.RadarPreHeaderEncoderBlock, _Mapping]]] = ...) -> None: ...
