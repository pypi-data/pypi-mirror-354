import datetime
import typing

import kubernetes.client

class V1alpha3CounterSet:
    counters: dict[str, kubernetes.client.V1alpha3Counter]
    name: str
    
    def __init__(self, *, counters: dict[str, kubernetes.client.V1alpha3Counter], name: str) -> None:
        ...
    def to_dict(self) -> V1alpha3CounterSetDict:
        ...
class V1alpha3CounterSetDict(typing.TypedDict, total=False):
    counters: dict[str, kubernetes.client.V1alpha3CounterDict]
    name: str
