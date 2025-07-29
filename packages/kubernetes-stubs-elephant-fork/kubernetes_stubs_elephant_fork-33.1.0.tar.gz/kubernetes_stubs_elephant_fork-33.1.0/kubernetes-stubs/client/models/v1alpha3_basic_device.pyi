import datetime
import typing

import kubernetes.client

class V1alpha3BasicDevice:
    all_nodes: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1alpha3DeviceAttribute]]
    capacity: typing.Optional[dict[str, str]]
    consumes_counters: typing.Optional[list[kubernetes.client.V1alpha3DeviceCounterConsumption]]
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    taints: typing.Optional[list[kubernetes.client.V1alpha3DeviceTaint]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., attributes: typing.Optional[dict[str, kubernetes.client.V1alpha3DeviceAttribute]] = ..., capacity: typing.Optional[dict[str, str]] = ..., consumes_counters: typing.Optional[list[kubernetes.client.V1alpha3DeviceCounterConsumption]] = ..., node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., taints: typing.Optional[list[kubernetes.client.V1alpha3DeviceTaint]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3BasicDeviceDict:
        ...
class V1alpha3BasicDeviceDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1alpha3DeviceAttributeDict]]
    capacity: typing.Optional[dict[str, str]]
    consumesCounters: typing.Optional[list[kubernetes.client.V1alpha3DeviceCounterConsumptionDict]]
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    taints: typing.Optional[list[kubernetes.client.V1alpha3DeviceTaintDict]]
