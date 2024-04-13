from http.server import BaseHTTPRequestHandler
from typing import Dict, Generic, List, Optional, TypeVar, cast

from server.handling.method import RequestMethod
from server.handling.request import Request
from server.handling.response import Response
from server.routing.route import Route
from server.routing.utils import route_path_to_trie_key, trie_route_search
from server.serve.baseserver import BaseServer


class ExtendedHTTPRequestHandler(BaseHTTPRequestHandler):

    server: BaseServer

    # Remove "Server" header.
    def send_response(self, code: int, message: str | None = None) -> None:
        self.send_response_only(code, message)
        # self.send_header('Server', self.version_string())
        self.send_header("Date", self.date_time_string())

    def method(self, method_string: str) -> None:
        param_values: List[str] = []

        route: Route = cast(
            Route,
            trie_route_search(
                self.server.routes,
                self.path,
                out_params=param_values,
            ),
        )

        # print(self.path, route)

        params: Dict[str, str] = dict()
        if route == None or not route.populate_params(param_values, out_params=params):
            self.send_response(404)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Not found.<h1>")
            return
        if route.handlers.get(method_string) == None:
            self.send_response(405)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Method not allowed.<h1>")
            return

        headers: Dict[str, str] = dict()
        header_keys = self.headers.keys()
        header_values = self.headers.values()
        for i, key in enumerate(header_keys):
            headers[key.lower()] = header_values[i]

        req: Request = Request(
            self.path, RequestMethod.GET, headers, self.server.state, params, self.rfile
        )
        res: Response = Response(self)

        route.handlers[method_string](req, res)

        # Maybe throw an error?
        if not res._sent:
            ...

    def do_GET(self) -> None:
        self.method("GET")

    def do_POST(self) -> None:
        self.method("POST")

    def do_PATCH(self) -> None:
        self.method("PATCH")

    def do_PUT(self) -> None:
        self.method("PUT")

    def do_DELETE(self) -> None:
        self.method("DELETE")
