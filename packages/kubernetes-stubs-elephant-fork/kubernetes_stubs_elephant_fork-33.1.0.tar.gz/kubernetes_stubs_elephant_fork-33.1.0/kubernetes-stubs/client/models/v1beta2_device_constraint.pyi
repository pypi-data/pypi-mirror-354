import datetime
import typing

import kubernetes.client

class V1beta2DeviceConstraint:
    match_attribute: typing.Optional[str]
    requests: typing.Optional[list[str]]
    
    def __init__(self, *, match_attribute: typing.Optional[str] = ..., requests: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceConstraintDict:
        ...
class V1beta2DeviceConstraintDict(typing.TypedDict, total=False):
    matchAttribute: typing.Optional[str]
    requests: typing.Optional[list[str]]
