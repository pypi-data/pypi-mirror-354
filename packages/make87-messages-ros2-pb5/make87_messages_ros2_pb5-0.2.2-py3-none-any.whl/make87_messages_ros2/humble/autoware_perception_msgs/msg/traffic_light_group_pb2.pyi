from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_perception_msgs.msg import traffic_light_element_pb2 as _traffic_light_element_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficLightGroup(_message.Message):
    __slots__ = ("header", "traffic_light_group_id", "elements")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_LIGHT_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    traffic_light_group_id: int
    elements: _containers.RepeatedCompositeFieldContainer[_traffic_light_element_pb2.TrafficLightElement]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., traffic_light_group_id: _Optional[int] = ..., elements: _Optional[_Iterable[_Union[_traffic_light_element_pb2.TrafficLightElement, _Mapping]]] = ...) -> None: ...
