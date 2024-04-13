from typing import Dict, Generic, TypeVar, TypedDict


ParamType = TypeVar("ParamType")


class Request(Generic[ParamType]):
    params: ParamType

    def __init__(self, params: ParamType):
        self.params = params
