from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.rmf_dispenser_msgs.msg import dispenser_request_item_pb2 as _dispenser_request_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispenserRequest(_message.Message):
    __slots__ = ("time", "request_guid", "target_guid", "transporter_type", "items")
    TIME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_GUID_FIELD_NUMBER: _ClassVar[int]
    TARGET_GUID_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    request_guid: str
    target_guid: str
    transporter_type: str
    items: _containers.RepeatedCompositeFieldContainer[_dispenser_request_item_pb2.DispenserRequestItem]
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., request_guid: _Optional[str] = ..., target_guid: _Optional[str] = ..., transporter_type: _Optional[str] = ..., items: _Optional[_Iterable[_Union[_dispenser_request_item_pb2.DispenserRequestItem, _Mapping]]] = ...) -> None: ...
