from enum import Enum


class RequestMethod(Enum):
    GET: int = 0
    POST: int = 1
    PUT: int = 2
    PATCH: int = 3
    DELETE: int = 4
