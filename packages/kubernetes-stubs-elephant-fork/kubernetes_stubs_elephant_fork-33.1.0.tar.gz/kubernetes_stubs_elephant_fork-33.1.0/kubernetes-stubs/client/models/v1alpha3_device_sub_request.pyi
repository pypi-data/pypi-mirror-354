import datetime
import typing

import kubernetes.client

class V1alpha3DeviceSubRequest:
    allocation_mode: typing.Optional[str]
    count: typing.Optional[int]
    device_class_name: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceToleration]]
    
    def __init__(self, *, allocation_mode: typing.Optional[str] = ..., count: typing.Optional[int] = ..., device_class_name: str, name: str, selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceSubRequestDict:
        ...
class V1alpha3DeviceSubRequestDict(typing.TypedDict, total=False):
    allocationMode: typing.Optional[str]
    count: typing.Optional[int]
    deviceClassName: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1alpha3DeviceTolerationDict]]
