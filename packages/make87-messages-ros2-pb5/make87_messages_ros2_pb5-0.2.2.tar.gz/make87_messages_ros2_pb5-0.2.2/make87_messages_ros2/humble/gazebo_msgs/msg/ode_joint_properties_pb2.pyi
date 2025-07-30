from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ODEJointProperties(_message.Message):
    __slots__ = ("header", "damping", "hi_stop", "lo_stop", "erp", "cfm", "stop_erp", "stop_cfm", "fudge_factor", "fmax", "vel")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DAMPING_FIELD_NUMBER: _ClassVar[int]
    HI_STOP_FIELD_NUMBER: _ClassVar[int]
    LO_STOP_FIELD_NUMBER: _ClassVar[int]
    ERP_FIELD_NUMBER: _ClassVar[int]
    CFM_FIELD_NUMBER: _ClassVar[int]
    STOP_ERP_FIELD_NUMBER: _ClassVar[int]
    STOP_CFM_FIELD_NUMBER: _ClassVar[int]
    FUDGE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    FMAX_FIELD_NUMBER: _ClassVar[int]
    VEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    damping: _containers.RepeatedScalarFieldContainer[float]
    hi_stop: _containers.RepeatedScalarFieldContainer[float]
    lo_stop: _containers.RepeatedScalarFieldContainer[float]
    erp: _containers.RepeatedScalarFieldContainer[float]
    cfm: _containers.RepeatedScalarFieldContainer[float]
    stop_erp: _containers.RepeatedScalarFieldContainer[float]
    stop_cfm: _containers.RepeatedScalarFieldContainer[float]
    fudge_factor: _containers.RepeatedScalarFieldContainer[float]
    fmax: _containers.RepeatedScalarFieldContainer[float]
    vel: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., damping: _Optional[_Iterable[float]] = ..., hi_stop: _Optional[_Iterable[float]] = ..., lo_stop: _Optional[_Iterable[float]] = ..., erp: _Optional[_Iterable[float]] = ..., cfm: _Optional[_Iterable[float]] = ..., stop_erp: _Optional[_Iterable[float]] = ..., stop_cfm: _Optional[_Iterable[float]] = ..., fudge_factor: _Optional[_Iterable[float]] = ..., fmax: _Optional[_Iterable[float]] = ..., vel: _Optional[_Iterable[float]] = ...) -> None: ...
