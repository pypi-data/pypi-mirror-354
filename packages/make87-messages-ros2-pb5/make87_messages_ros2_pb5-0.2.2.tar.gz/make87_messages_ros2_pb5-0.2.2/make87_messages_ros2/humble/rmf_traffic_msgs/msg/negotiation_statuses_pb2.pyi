from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import negotiation_status_pb2 as _negotiation_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationStatuses(_message.Message):
    __slots__ = ("header", "negotiations")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    negotiations: _containers.RepeatedCompositeFieldContainer[_negotiation_status_pb2.NegotiationStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., negotiations: _Optional[_Iterable[_Union[_negotiation_status_pb2.NegotiationStatus, _Mapping]]] = ...) -> None: ...
