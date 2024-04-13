from http.server import ThreadingHTTPServer
from typing import Any, Generic, TypeVar

from server.routing.route import Route
from structs.prefixtree.tree import PrefixTree

T = TypeVar("T")
class BaseServer(Generic[T], ThreadingHTTPServer):

    routes: PrefixTree[Route]
    state: T

    def __init__(
        self,
        server_address: Any,
        RequestHandlerClass: Any,
        routes: PrefixTree[Route],
        state: T,
        bind_and_activate: bool = True,
    ) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.routes = routes
        self.state = state