from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.shape_msgs.msg import mesh_pb2 as _mesh_pb2
from make87_messages_ros2.humble.shape_msgs.msg import solid_primitive_pb2 as _solid_primitive_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingVolume(_message.Message):
    __slots__ = ("header", "primitives", "primitive_poses", "meshes", "mesh_poses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVES_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_POSES_FIELD_NUMBER: _ClassVar[int]
    MESHES_FIELD_NUMBER: _ClassVar[int]
    MESH_POSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    primitives: _containers.RepeatedCompositeFieldContainer[_solid_primitive_pb2.SolidPrimitive]
    primitive_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    meshes: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.Mesh]
    mesh_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., primitives: _Optional[_Iterable[_Union[_solid_primitive_pb2.SolidPrimitive, _Mapping]]] = ..., primitive_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., meshes: _Optional[_Iterable[_Union[_mesh_pb2.Mesh, _Mapping]]] = ..., mesh_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ...) -> None: ...
