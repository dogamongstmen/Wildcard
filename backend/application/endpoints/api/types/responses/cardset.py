from typing import List, Optional
from application.endpoints.api.types.base import SerializableResponse

from pymongo.cursor import Cursor

from db.types.cardset import CardSet


class CardSetResponse(SerializableResponse):
    name: str
    cover_img: Optional[str]
    card_ids: List[str]

    def __init__(self, card_set: CardSet) -> None:
        super().__init__()
        self.name = card_set["name"]
        self.cover_img = card_set["cover_img"]
        self.card_ids = [str(cid) for cid in card_set["card_ids"]]


class CardSetCollectionResponse(SerializableResponse):
    card_sets: List[CardSetResponse]

    def __init__(self, card_sets: Cursor[CardSet]) -> None:
        super().__init__()
        self.sets = [CardSetResponse(card_set) for card_set in card_sets]
