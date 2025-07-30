from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MagneticFieldReading(_message.Message):
    __slots__ = ("timestamp", "x_gauss", "y_gauss", "z_gauss")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    X_GAUSS_FIELD_NUMBER: _ClassVar[int]
    Y_GAUSS_FIELD_NUMBER: _ClassVar[int]
    Z_GAUSS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    x_gauss: float
    y_gauss: float
    z_gauss: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., x_gauss: _Optional[float] = ..., y_gauss: _Optional[float] = ..., z_gauss: _Optional[float] = ...) -> None: ...
