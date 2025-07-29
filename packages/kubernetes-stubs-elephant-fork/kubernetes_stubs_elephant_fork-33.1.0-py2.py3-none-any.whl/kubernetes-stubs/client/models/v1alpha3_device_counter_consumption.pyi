import datetime
import typing

import kubernetes.client

class V1alpha3DeviceCounterConsumption:
    counter_set: str
    counters: dict[str, kubernetes.client.V1alpha3Counter]
    
    def __init__(self, *, counter_set: str, counters: dict[str, kubernetes.client.V1alpha3Counter]) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceCounterConsumptionDict:
        ...
class V1alpha3DeviceCounterConsumptionDict(typing.TypedDict, total=False):
    counterSet: str
    counters: dict[str, kubernetes.client.V1alpha3CounterDict]
