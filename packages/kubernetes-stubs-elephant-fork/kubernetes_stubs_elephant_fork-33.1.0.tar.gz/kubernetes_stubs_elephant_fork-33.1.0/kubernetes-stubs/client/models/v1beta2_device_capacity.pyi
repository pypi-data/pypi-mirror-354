import datetime
import typing

import kubernetes.client

class V1beta2DeviceCapacity:
    value: str
    
    def __init__(self, *, value: str) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceCapacityDict:
        ...
class V1beta2DeviceCapacityDict(typing.TypedDict, total=False):
    value: str
