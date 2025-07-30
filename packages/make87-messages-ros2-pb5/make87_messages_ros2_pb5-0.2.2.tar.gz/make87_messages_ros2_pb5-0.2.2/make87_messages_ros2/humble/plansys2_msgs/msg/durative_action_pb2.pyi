from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import param_pb2 as _param_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DurativeAction(_message.Message):
    __slots__ = ("header", "name", "parameters", "at_start_requirements", "over_all_requirements", "at_end_requirements", "at_start_effects", "at_end_effects")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    AT_START_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    OVER_ALL_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    AT_END_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    AT_START_EFFECTS_FIELD_NUMBER: _ClassVar[int]
    AT_END_EFFECTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    parameters: _containers.RepeatedCompositeFieldContainer[_param_pb2.Param]
    at_start_requirements: _tree_pb2.Tree
    over_all_requirements: _tree_pb2.Tree
    at_end_requirements: _tree_pb2.Tree
    at_start_effects: _tree_pb2.Tree
    at_end_effects: _tree_pb2.Tree
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_param_pb2.Param, _Mapping]]] = ..., at_start_requirements: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ..., over_all_requirements: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ..., at_end_requirements: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ..., at_start_effects: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ..., at_end_effects: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ...) -> None: ...
