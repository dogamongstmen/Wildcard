from typing import Callable, TypeVar

from server.handling.request import Request
from server.handling.response import Response

S = TypeVar("S")
P = TypeVar("P")

RequestHandler = Callable[[S, Request[P], Response], None]


def default_404_handler(state: S, req: Request, res: Response) -> None:
    res.status(404).html("Not found")
