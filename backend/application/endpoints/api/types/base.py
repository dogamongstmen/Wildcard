from typing import Any, Dict


class SerializableResponse:
    def __init__(self) -> None: ...
    def to_serializable(self) -> Dict[str, Any]:
        return self.__dict__
