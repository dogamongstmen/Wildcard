from socket import SHUT_RDWR, socket
from threading import Thread
from typing import Generic, Optional, Self, Tuple, TypeVar, cast

from commontypes.boolean import false, true
from server.handling.handler import RequestHandler, default_404_handler
from server.routing.route import Route
from server.routing.utils import route_path_to_trie_key
from server.serve.internalhandler import ExtendedHTTPRequestHandler
from server.serve.internalserver import ExtendedHTTPServer
from structs.prefixtree.tree import PrefixTree

Socket = socket

StateType = TypeVar("StateType")


class Server(Generic[StateType]):

    _listening_thread: Optional[Thread]
    __is_listening: bool
    __server: Optional[ExtendedHTTPServer]

    state: StateType
    routes: PrefixTree[Route]

    not_found_handler: RequestHandler

    def __init__(self, state: StateType) -> None:
        super().__init__()
        self.state = state
        self.routes = PrefixTree()
        self.__is_listening = false
        self._listening_thread = None
        self.__server = None
        self.not_found_handler = default_404_handler

    def route(self, route: Route) -> Self:
        self.routes.insert(route_path_to_trie_key(route.path), route)
        return self

    def not_found(self, handler: RequestHandler) -> Self:
        self.not_found_handler = handler
        return self

    def shutdown(self, socket: Socket) -> None:
        cast(ExtendedHTTPServer, self.__server).shutdown()
        cast(Thread, self._listening_thread).join()

    def listen(self, address: str, port: int) -> Optional[Socket]:
        if self.__is_listening:
            return None

        self.__server = ExtendedHTTPServer(
            (
                address,
                port,
            ),
            ExtendedHTTPRequestHandler,
            self.routes,
            self.state,
            self.not_found_handler,
        )
        # self.__server.serve_forever()
        self._listening_thread = Thread(target=self.__server.serve_forever, daemon=true)
        self._listening_thread.start()

        return self.__server.socket
