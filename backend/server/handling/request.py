from typing import BinaryIO, Dict, Generic, TypeVar, TypedDict

from server.handling.method import RequestMethod


ParamType = TypeVar("ParamType")


class Request(Generic[ParamType]):

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
        params: ParamType,
        buffer: BinaryIO,
    ):
        self.params = params

        self.path = path
        self.method = method
        self.headers = headers
        self._buffer = buffer
