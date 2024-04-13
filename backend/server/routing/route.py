from typing import Dict, List, Self
from server.handling.handler import RequestHandler


class Route:

    handlers: Dict[str, RequestHandler]

    path: str
    params: List[str]

    def __init__(self, path: str) -> None:
        self.path = path
        self.handlers = dict()
        self.params = [
            substr[1 : len(substr)]
            for substr in path.split("/")
            if len(substr) > 1 and substr.startswith(":")
        ]

    def get(self, handler: RequestHandler) -> Self:
        self.handlers["GET"] = handler
        return self

    def post(self, handler: RequestHandler) -> Self:
        self.handlers["POST"] = handler
        return self

    def patch(self, handler: RequestHandler) -> Self:
        self.handlers["PATCH"] = handler
        return self

    def put(self, handler: RequestHandler) -> Self:
        self.handlers["PUT"] = handler
        return self

    def delete(self, handler: RequestHandler) -> Self:
        self.handlers["DELETE"] = handler
        return self

    def populate_params(self, param_values: List[str]) -> Dict[str, str]:
        params: Dict[str, str] = dict()
        for i, param in enumerate(self.params):
            params[param] = param_values[i]
        return params
