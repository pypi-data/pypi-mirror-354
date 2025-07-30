from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackstatChannel(_message.Message):
    __slots__ = ("header", "prn", "glofreq", "ch_tr_status", "psr", "doppler", "c_no", "locktime", "psr_res", "reject", "psr_weight")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRN_FIELD_NUMBER: _ClassVar[int]
    GLOFREQ_FIELD_NUMBER: _ClassVar[int]
    CH_TR_STATUS_FIELD_NUMBER: _ClassVar[int]
    PSR_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_FIELD_NUMBER: _ClassVar[int]
    C_NO_FIELD_NUMBER: _ClassVar[int]
    LOCKTIME_FIELD_NUMBER: _ClassVar[int]
    PSR_RES_FIELD_NUMBER: _ClassVar[int]
    REJECT_FIELD_NUMBER: _ClassVar[int]
    PSR_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    prn: int
    glofreq: int
    ch_tr_status: int
    psr: float
    doppler: float
    c_no: float
    locktime: float
    psr_res: float
    reject: str
    psr_weight: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., prn: _Optional[int] = ..., glofreq: _Optional[int] = ..., ch_tr_status: _Optional[int] = ..., psr: _Optional[float] = ..., doppler: _Optional[float] = ..., c_no: _Optional[float] = ..., locktime: _Optional[float] = ..., psr_res: _Optional[float] = ..., reject: _Optional[str] = ..., psr_weight: _Optional[float] = ...) -> None: ...
