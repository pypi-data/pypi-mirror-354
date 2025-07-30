from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_perception_msgs.msg import object_classification_pb2 as _object_classification_pb2
from make87_messages_ros2.humble.autoware_perception_msgs.msg import shape_pb2 as _shape_pb2
from make87_messages_ros2.humble.autoware_perception_msgs.msg import tracked_object_kinematics_pb2 as _tracked_object_kinematics_pb2
from make87_messages_ros2.humble.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackedObject(_message.Message):
    __slots__ = ("header", "object_id", "existence_probability", "classification", "kinematics", "shape")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXISTENCE_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    KINEMATICS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    object_id: _uuid_pb2.UUID
    existence_probability: float
    classification: _containers.RepeatedCompositeFieldContainer[_object_classification_pb2.ObjectClassification]
    kinematics: _tracked_object_kinematics_pb2.TrackedObjectKinematics
    shape: _shape_pb2.Shape
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., object_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., existence_probability: _Optional[float] = ..., classification: _Optional[_Iterable[_Union[_object_classification_pb2.ObjectClassification, _Mapping]]] = ..., kinematics: _Optional[_Union[_tracked_object_kinematics_pb2.TrackedObjectKinematics, _Mapping]] = ..., shape: _Optional[_Union[_shape_pb2.Shape, _Mapping]] = ...) -> None: ...
