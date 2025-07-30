from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_extended_solution_status_pb2 as _novatel_extended_solution_status_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_signal_mask_pb2 as _novatel_signal_mask_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelUtmPosition(_message.Message):
    __slots__ = ("header", "ros2_header", "novatel_msg_header", "solution_status", "position_type", "lon_zone_number", "lat_zone_letter", "northing", "easting", "height", "undulation", "datum_id", "northing_sigma", "easting_sigma", "height_sigma", "base_station_id", "diff_age", "solution_age", "num_satellites_tracked", "num_satellites_used_in_solution", "num_gps_and_glonass_l1_used_in_solution", "num_gps_and_glonass_l1_and_l2_used_in_solution", "extended_solution_status", "signal_mask")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    LON_ZONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LAT_ZONE_LETTER_FIELD_NUMBER: _ClassVar[int]
    NORTHING_FIELD_NUMBER: _ClassVar[int]
    EASTING_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    DATUM_ID_FIELD_NUMBER: _ClassVar[int]
    NORTHING_SIGMA_FIELD_NUMBER: _ClassVar[int]
    EASTING_SIGMA_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_SIGMA_FIELD_NUMBER: _ClassVar[int]
    BASE_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIFF_AGE_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_AGE_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_TRACKED_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    NUM_GPS_AND_GLONASS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    NUM_GPS_AND_GLONASS_L1_AND_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    solution_status: str
    position_type: str
    lon_zone_number: int
    lat_zone_letter: str
    northing: float
    easting: float
    height: float
    undulation: float
    datum_id: str
    northing_sigma: float
    easting_sigma: float
    height_sigma: float
    base_station_id: str
    diff_age: float
    solution_age: float
    num_satellites_tracked: int
    num_satellites_used_in_solution: int
    num_gps_and_glonass_l1_used_in_solution: int
    num_gps_and_glonass_l1_and_l2_used_in_solution: int
    extended_solution_status: _novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus
    signal_mask: _novatel_signal_mask_pb2.NovatelSignalMask
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., solution_status: _Optional[str] = ..., position_type: _Optional[str] = ..., lon_zone_number: _Optional[int] = ..., lat_zone_letter: _Optional[str] = ..., northing: _Optional[float] = ..., easting: _Optional[float] = ..., height: _Optional[float] = ..., undulation: _Optional[float] = ..., datum_id: _Optional[str] = ..., northing_sigma: _Optional[float] = ..., easting_sigma: _Optional[float] = ..., height_sigma: _Optional[float] = ..., base_station_id: _Optional[str] = ..., diff_age: _Optional[float] = ..., solution_age: _Optional[float] = ..., num_satellites_tracked: _Optional[int] = ..., num_satellites_used_in_solution: _Optional[int] = ..., num_gps_and_glonass_l1_used_in_solution: _Optional[int] = ..., num_gps_and_glonass_l1_and_l2_used_in_solution: _Optional[int] = ..., extended_solution_status: _Optional[_Union[_novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus, _Mapping]] = ..., signal_mask: _Optional[_Union[_novatel_signal_mask_pb2.NovatelSignalMask, _Mapping]] = ...) -> None: ...
