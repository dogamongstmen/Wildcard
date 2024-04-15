from application.endpoints.api.types.base import SerializableResponse
from db.types.card import Flashcard


class FlashcardResponse(SerializableResponse):
    q: str
    a: str

    def __init__(self, f: Flashcard) -> None:
        super().__init__()
        self.q = f["q"]
        self.a = f["a"]
