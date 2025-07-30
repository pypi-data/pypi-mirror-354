from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import bid_proposal_pb2 as _bid_proposal_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BidResponse(_message.Message):
    __slots__ = ("header", "task_id", "has_proposal", "proposal", "errors")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    has_proposal: bool
    proposal: _bid_proposal_pb2.BidProposal
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., has_proposal: bool = ..., proposal: _Optional[_Union[_bid_proposal_pb2.BidProposal, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...
