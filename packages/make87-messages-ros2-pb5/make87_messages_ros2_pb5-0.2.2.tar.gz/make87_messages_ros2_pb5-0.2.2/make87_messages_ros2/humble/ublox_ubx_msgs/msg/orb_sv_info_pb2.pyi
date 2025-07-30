from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import orb_alm_info_pb2 as _orb_alm_info_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import orb_eph_info_pb2 as _orb_eph_info_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import orb_sv_flag_pb2 as _orb_sv_flag_pb2
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import other_orb_info_pb2 as _other_orb_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrbSVInfo(_message.Message):
    __slots__ = ("header", "gnss_id", "sv_id", "sv_flag", "eph", "alm", "other_orb")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    SV_FLAG_FIELD_NUMBER: _ClassVar[int]
    EPH_FIELD_NUMBER: _ClassVar[int]
    ALM_FIELD_NUMBER: _ClassVar[int]
    OTHER_ORB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gnss_id: int
    sv_id: int
    sv_flag: _orb_sv_flag_pb2.OrbSVFlag
    eph: _orb_eph_info_pb2.OrbEphInfo
    alm: _orb_alm_info_pb2.OrbAlmInfo
    other_orb: _other_orb_info_pb2.OtherOrbInfo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., sv_flag: _Optional[_Union[_orb_sv_flag_pb2.OrbSVFlag, _Mapping]] = ..., eph: _Optional[_Union[_orb_eph_info_pb2.OrbEphInfo, _Mapping]] = ..., alm: _Optional[_Union[_orb_alm_info_pb2.OrbAlmInfo, _Mapping]] = ..., other_orb: _Optional[_Union[_other_orb_info_pb2.OtherOrbInfo, _Mapping]] = ...) -> None: ...
