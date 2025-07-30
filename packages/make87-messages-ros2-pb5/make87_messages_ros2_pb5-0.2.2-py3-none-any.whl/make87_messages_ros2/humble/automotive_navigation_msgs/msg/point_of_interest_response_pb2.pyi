from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.automotive_navigation_msgs.msg import point_of_interest_status_pb2 as _point_of_interest_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointOfInterestResponse(_message.Message):
    __slots__ = ("header", "ros2_header", "name", "module_name", "request_id", "update_num", "point_statuses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_NUM_FIELD_NUMBER: _ClassVar[int]
    POINT_STATUSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    name: str
    module_name: str
    request_id: int
    update_num: int
    point_statuses: _containers.RepeatedCompositeFieldContainer[_point_of_interest_status_pb2.PointOfInterestStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., name: _Optional[str] = ..., module_name: _Optional[str] = ..., request_id: _Optional[int] = ..., update_num: _Optional[int] = ..., point_statuses: _Optional[_Iterable[_Union[_point_of_interest_status_pb2.PointOfInterestStatus, _Mapping]]] = ...) -> None: ...
