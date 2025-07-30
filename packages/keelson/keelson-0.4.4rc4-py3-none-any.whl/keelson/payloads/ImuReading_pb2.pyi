from google.protobuf import timestamp_pb2 as _timestamp_pb2
from foxglove import Vector3_pb2 as _Vector3_pb2
from foxglove import Quaternion_pb2 as _Quaternion_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImuReading(_message.Message):
    __slots__ = ("timestamp", "frame_id", "orientation", "orientation_covariance", "angular_velocity", "angular_velocity_covariance", "linear_acceleration", "linear_acceleration_covariance")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    frame_id: str
    orientation: _Quaternion_pb2.Quaternion
    orientation_covariance: _containers.RepeatedScalarFieldContainer[float]
    angular_velocity: _Vector3_pb2.Vector3
    angular_velocity_covariance: _containers.RepeatedScalarFieldContainer[float]
    linear_acceleration: _Vector3_pb2.Vector3
    linear_acceleration_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., frame_id: _Optional[str] = ..., orientation: _Optional[_Union[_Quaternion_pb2.Quaternion, _Mapping]] = ..., orientation_covariance: _Optional[_Iterable[float]] = ..., angular_velocity: _Optional[_Union[_Vector3_pb2.Vector3, _Mapping]] = ..., angular_velocity_covariance: _Optional[_Iterable[float]] = ..., linear_acceleration: _Optional[_Union[_Vector3_pb2.Vector3, _Mapping]] = ..., linear_acceleration_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
