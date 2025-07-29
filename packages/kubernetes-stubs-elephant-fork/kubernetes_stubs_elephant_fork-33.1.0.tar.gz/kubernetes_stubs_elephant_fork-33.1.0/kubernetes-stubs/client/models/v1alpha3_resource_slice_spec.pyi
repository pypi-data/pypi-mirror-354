import datetime
import typing

import kubernetes.client

class V1alpha3ResourceSliceSpec:
    all_nodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1alpha3Device]]
    driver: str
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    per_device_node_selection: typing.Optional[bool]
    pool: kubernetes.client.V1alpha3ResourcePool
    shared_counters: typing.Optional[list[kubernetes.client.V1alpha3CounterSet]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., devices: typing.Optional[list[kubernetes.client.V1alpha3Device]] = ..., driver: str, node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., per_device_node_selection: typing.Optional[bool] = ..., pool: kubernetes.client.V1alpha3ResourcePool, shared_counters: typing.Optional[list[kubernetes.client.V1alpha3CounterSet]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceSliceSpecDict:
        ...
class V1alpha3ResourceSliceSpecDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1alpha3DeviceDict]]
    driver: str
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    perDeviceNodeSelection: typing.Optional[bool]
    pool: kubernetes.client.V1alpha3ResourcePoolDict
    sharedCounters: typing.Optional[list[kubernetes.client.V1alpha3CounterSetDict]]
