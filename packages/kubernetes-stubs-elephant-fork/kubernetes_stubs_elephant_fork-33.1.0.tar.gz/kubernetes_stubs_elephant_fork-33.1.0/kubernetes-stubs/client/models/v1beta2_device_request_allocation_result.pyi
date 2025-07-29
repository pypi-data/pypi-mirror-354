import datetime
import typing

import kubernetes.client

class V1beta2DeviceRequestAllocationResult:
    admin_access: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., device: str, driver: str, pool: str, request: str, tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceRequestAllocationResultDict:
        ...
class V1beta2DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceTolerationDict]]
