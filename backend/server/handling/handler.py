from typing import Callable, TypeVar

from server.handling.request import Request
from server.handling.response import Response

S = TypeVar("S")
P = TypeVar("P")

RequestHandler = Callable[[Request[S, P], Response], None]
