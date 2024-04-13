from typing import BinaryIO, Dict, Generic, TypeVar, TypedDict

from server.handling.method import RequestMethod


StateType = TypeVar("StateType")
ParamType = TypeVar("ParamType")


class Request(Generic[StateType, ParamType]):

    state: StateType

    path: str
    method: RequestMethod
    headers: Dict[str, str]

    _buffer: BinaryIO

    params: ParamType

    def __init__(
        self,
        path: str,
        method: RequestMethod,
        headers: Dict[str, str],
        state: StateType,
        params: ParamType,
        buffer: BinaryIO,
    ):
        self.state = state
        self.params = params

        self.path = path
        self.method = method
        self.headers = headers
        self._buffer = buffer
