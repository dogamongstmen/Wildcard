from typing import Callable, TypeVar

from server.handling.request import Request
from server.handling.response import Response

S = TypeVar("S")
P = TypeVar("P")

RequestHandler = Callable[[Request[S, P], Response], None]


def default_404_handler(req: Request, res: Response) -> None:
    res.status(404).html("Not found")
