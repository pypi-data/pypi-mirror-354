from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gyro(_message.Message):
    __slots__ = ("timestamp", "x_radps", "y_radps", "z_radps")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    X_RADPS_FIELD_NUMBER: _ClassVar[int]
    Y_RADPS_FIELD_NUMBER: _ClassVar[int]
    Z_RADPS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    x_radps: float
    y_radps: float
    z_radps: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., x_radps: _Optional[float] = ..., y_radps: _Optional[float] = ..., z_radps: _Optional[float] = ...) -> None: ...
