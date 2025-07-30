from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Lane(_message.Message):
    __slots__ = ("quality", "marker_kind", "curve_model_kind", "marker_offset", "heading_angle", "curvature", "curvature_derivative", "marker_width", "view_range")
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    MARKER_KIND_FIELD_NUMBER: _ClassVar[int]
    CURVE_MODEL_KIND_FIELD_NUMBER: _ClassVar[int]
    MARKER_OFFSET_FIELD_NUMBER: _ClassVar[int]
    HEADING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_FIELD_NUMBER: _ClassVar[int]
    CURVATURE_DERIVATIVE_FIELD_NUMBER: _ClassVar[int]
    MARKER_WIDTH_FIELD_NUMBER: _ClassVar[int]
    VIEW_RANGE_FIELD_NUMBER: _ClassVar[int]
    quality: int
    marker_kind: int
    curve_model_kind: int
    marker_offset: float
    heading_angle: float
    curvature: float
    curvature_derivative: float
    marker_width: float
    view_range: float
    def __init__(self, quality: _Optional[int] = ..., marker_kind: _Optional[int] = ..., curve_model_kind: _Optional[int] = ..., marker_offset: _Optional[float] = ..., heading_angle: _Optional[float] = ..., curvature: _Optional[float] = ..., curvature_derivative: _Optional[float] = ..., marker_width: _Optional[float] = ..., view_range: _Optional[float] = ...) -> None: ...
