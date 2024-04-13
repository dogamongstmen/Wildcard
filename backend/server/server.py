from socket import socket
from threading import Thread
from typing import Generic, Optional, Tuple, TypeVar

from commontypes.boolean import false, true
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

    def __init__(self, state: StateType) -> None:
        super().__init__()
        self.state = state
        self.routes = PrefixTree()
        self.__is_listening = false
        self._listening_thread = None
        self.__server = None

    def route(self, route: Route):
        self.routes.insert(route_path_to_trie_key(route.path), route)

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
        )
        # self.__server.serve_forever()
        self._listening_thread = Thread(target=self.__server.serve_forever, daemon=true)
        self._listening_thread.start()

        return self.__server.socket
