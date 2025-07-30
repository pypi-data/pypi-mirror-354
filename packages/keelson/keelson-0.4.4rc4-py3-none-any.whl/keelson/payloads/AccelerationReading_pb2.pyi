from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Acceleration(_message.Message):
    __slots__ = ("timestamp", "x_mpss", "y_mpss", "z_mpss")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    X_MPSS_FIELD_NUMBER: _ClassVar[int]
    Y_MPSS_FIELD_NUMBER: _ClassVar[int]
    Z_MPSS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    x_mpss: float
    y_mpss: float
    z_mpss: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., x_mpss: _Optional[float] = ..., y_mpss: _Optional[float] = ..., z_mpss: _Optional[float] = ...) -> None: ...
