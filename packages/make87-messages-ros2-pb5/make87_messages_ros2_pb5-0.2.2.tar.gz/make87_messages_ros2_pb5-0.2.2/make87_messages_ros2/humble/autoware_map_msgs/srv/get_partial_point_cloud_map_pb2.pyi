from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_map_msgs.msg import area_info_pb2 as _area_info_pb2
from make87_messages_ros2.humble.autoware_map_msgs.msg import point_cloud_map_cell_with_id_pb2 as _point_cloud_map_cell_with_id_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPartialPointCloudMapRequest(_message.Message):
    __slots__ = ("header", "area")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    area: _area_info_pb2.AreaInfo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., area: _Optional[_Union[_area_info_pb2.AreaInfo, _Mapping]] = ...) -> None: ...

class GetPartialPointCloudMapResponse(_message.Message):
    __slots__ = ("header", "ros2_header", "new_pointcloud_with_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NEW_POINTCLOUD_WITH_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    new_pointcloud_with_ids: _containers.RepeatedCompositeFieldContainer[_point_cloud_map_cell_with_id_pb2.PointCloudMapCellWithID]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., new_pointcloud_with_ids: _Optional[_Iterable[_Union[_point_cloud_map_cell_with_id_pb2.PointCloudMapCellWithID, _Mapping]]] = ...) -> None: ...
