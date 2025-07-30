from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteRobotStateFromWarehouseRequest(_message.Message):
    __slots__ = ("name", "robot")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    name: str
    robot: str
    def __init__(self, name: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class DeleteRobotStateFromWarehouseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
