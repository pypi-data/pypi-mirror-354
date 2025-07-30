from make87_messages_ros2.jazzy.nav2_msgs.msg import costmap_meta_data_pb2 as _costmap_meta_data_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Costmap(_message.Message):
    __slots__ = ("header", "metadata", "data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    metadata: _costmap_meta_data_pb2.CostmapMetaData
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., metadata: _Optional[_Union[_costmap_meta_data_pb2.CostmapMetaData, _Mapping]] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
