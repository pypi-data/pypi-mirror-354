import datetime
import typing

import kubernetes.client

class V1alpha3DeviceRequestAllocationResult:
    admin_access: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., device: str, driver: str, pool: str, request: str, tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceRequestAllocationResultDict:
        ...
class V1alpha3DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceTolerationDict]]
