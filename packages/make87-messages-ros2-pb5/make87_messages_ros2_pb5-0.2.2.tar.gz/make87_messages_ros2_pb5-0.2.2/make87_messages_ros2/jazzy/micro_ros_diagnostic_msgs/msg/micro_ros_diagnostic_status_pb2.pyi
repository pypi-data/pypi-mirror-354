from make87_messages_ros2.jazzy.micro_ros_diagnostic_msgs.msg import micro_ros_diagnostic_key_value_pb2 as _micro_ros_diagnostic_key_value_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MicroROSDiagnosticStatus(_message.Message):
    __slots__ = ("level", "updater_id", "hardware_id", "number_of_values", "values")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    UPDATER_ID_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_VALUES_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    level: int
    updater_id: int
    hardware_id: int
    number_of_values: int
    values: _containers.RepeatedCompositeFieldContainer[_micro_ros_diagnostic_key_value_pb2.MicroROSDiagnosticKeyValue]
    def __init__(self, level: _Optional[int] = ..., updater_id: _Optional[int] = ..., hardware_id: _Optional[int] = ..., number_of_values: _Optional[int] = ..., values: _Optional[_Iterable[_Union[_micro_ros_diagnostic_key_value_pb2.MicroROSDiagnosticKeyValue, _Mapping]]] = ...) -> None: ...
