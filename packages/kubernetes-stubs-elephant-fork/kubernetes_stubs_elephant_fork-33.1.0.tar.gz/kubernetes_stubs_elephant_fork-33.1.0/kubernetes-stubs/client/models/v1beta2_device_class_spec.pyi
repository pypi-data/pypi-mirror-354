import datetime
import typing

import kubernetes.client

class V1beta2DeviceClassSpec:
    config: typing.Optional[list[kubernetes.client.V1beta2DeviceClassConfiguration]]
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1beta2DeviceClassConfiguration]] = ..., selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceClassSpecDict:
        ...
class V1beta2DeviceClassSpecDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1beta2DeviceClassConfigurationDict]]
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelectorDict]]
