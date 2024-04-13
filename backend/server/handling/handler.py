from typing import Callable, TypeVar

from server.handling.request import Request
from server.handling.response import Response

T = TypeVar("T")
RequestHandler = Callable[[Request[T], Response], None]
