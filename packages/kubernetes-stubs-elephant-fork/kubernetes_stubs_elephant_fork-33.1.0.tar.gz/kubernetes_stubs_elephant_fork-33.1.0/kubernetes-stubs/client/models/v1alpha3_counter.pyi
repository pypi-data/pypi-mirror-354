import datetime
import typing

import kubernetes.client

class V1alpha3Counter:
    value: str
    
    def __init__(self, *, value: str) -> None:
        ...
    def to_dict(self) -> V1alpha3CounterDict:
        ...
class V1alpha3CounterDict(typing.TypedDict, total=False):
    value: str
