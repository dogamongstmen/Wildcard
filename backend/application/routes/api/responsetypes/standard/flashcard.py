from typing import cast
from bson import ObjectId
from pymongo.collection import Collection

from application.routes.api.responsetypes.base import SerializableResponse
from db.types.card import Flashcard


class CreatedFlashcardResponse(SerializableResponse):
    card_id: str

    def __init__(self, id: ObjectId) -> None:
        super().__init__()
        self.card_id = str(id)


class FlashcardResponse(SerializableResponse):
    q: str
    a: str

    def __init__(self, f: Flashcard) -> None:
        super().__init__()
        self.q = f["q"]
        self.a = f["a"]
        # self.id = str(f["_id"])

