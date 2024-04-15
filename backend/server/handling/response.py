from http.server import BaseHTTPRequestHandler
import json
from typing import Any, Dict, Self

from common.types.boolean import false, true


class Response:

    _sent: bool
    __handler_ref: BaseHTTPRequestHandler

    __status_code: int = 200
    headers: Dict[str, str]

    def __init__(self, ref: BaseHTTPRequestHandler) -> None:
        self._sent = false
        self.__handler_ref = ref

        self.headers = dict()

    def header(self, key: str, value: str) -> Self:
        self.headers[key.lower()] = value
        return self

    def status(self, code: int) -> Self:
        self.__status_code = code
        return self

    def html(self, html: str):
        self.header("content-type", "text/html")
        self.send(bytearray(html, "utf-8"))

    def json(self, obj: Dict[str, Any]):
        self.header("content-type", "application/json")
        self.send(bytearray(json.dumps(obj), "utf-8"))

    def send(self, buffer: bytearray) -> None:
        if self._sent:
            return

        self._sent = true

        self.__handler_ref.send_response(self.__status_code)

        for key in self.headers:
            self.__handler_ref.send_header(key, self.headers[key])
        self.__handler_ref.end_headers()

        self.__handler_ref.wfile.write(buffer)

    def close(self):
        self.__handler_ref.wfile.close()
