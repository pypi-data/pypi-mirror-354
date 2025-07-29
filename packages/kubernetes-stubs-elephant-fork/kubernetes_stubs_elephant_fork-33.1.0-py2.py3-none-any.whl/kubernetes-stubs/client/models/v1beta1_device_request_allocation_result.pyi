import datetime
import typing

import kubernetes.client

class V1beta1DeviceRequestAllocationResult:
    admin_access: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., device: str, driver: str, pool: str, request: str, tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceRequestAllocationResultDict:
        ...
class V1beta1DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceTolerationDict]]
