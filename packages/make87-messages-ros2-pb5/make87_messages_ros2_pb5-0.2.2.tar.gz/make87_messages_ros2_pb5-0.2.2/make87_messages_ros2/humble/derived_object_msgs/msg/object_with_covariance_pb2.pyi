from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.derived_object_msgs.msg import solid_primitive_with_covariance_pb2 as _solid_primitive_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import accel_with_covariance_pb2 as _accel_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import polygon_pb2 as _polygon_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectWithCovariance(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "detection_level", "object_classified", "pose", "twist", "accel", "polygon", "shape", "classification", "classification_certainty", "classification_age")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DETECTION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASSIFIED_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    ACCEL_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_CERTAINTY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_AGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    detection_level: int
    object_classified: bool
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    twist: _twist_with_covariance_pb2.TwistWithCovariance
    accel: _accel_with_covariance_pb2.AccelWithCovariance
    polygon: _polygon_pb2.Polygon
    shape: _solid_primitive_with_covariance_pb2.SolidPrimitiveWithCovariance
    classification: int
    classification_certainty: int
    classification_age: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., detection_level: _Optional[int] = ..., object_classified: bool = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., twist: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., accel: _Optional[_Union[_accel_with_covariance_pb2.AccelWithCovariance, _Mapping]] = ..., polygon: _Optional[_Union[_polygon_pb2.Polygon, _Mapping]] = ..., shape: _Optional[_Union[_solid_primitive_with_covariance_pb2.SolidPrimitiveWithCovariance, _Mapping]] = ..., classification: _Optional[int] = ..., classification_certainty: _Optional[int] = ..., classification_age: _Optional[int] = ...) -> None: ...
