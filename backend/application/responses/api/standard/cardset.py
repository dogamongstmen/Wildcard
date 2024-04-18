from typing import Any, Dict, Optional

from bson import ObjectId
from application.responses.api.base import SerializableResponse
from db.db import DbCursor
from db.types.card import Flashcard
from db.types.cardset import CardSet


class CardSetMembersResponse(SerializableResponse):
    cards: Dict[str, Dict[str, Any]]

    def __init__(self, cards: DbCursor[Flashcard]) -> None:
        super().__init__()

        self.cards = dict()
        for card in cards:
            self.cards[str(card["_id"])] = {
                "q": card["q"],
                "a": card["a"],
            }
            # self.cards[str(card["_id"])]["q"] = card["q"]
            # self.cards[str(card["_id"])]["a"] = card["a"]
            # self.cards[str(card["_id"])]["parent_id"] = str(card["parent_id"])


class CardSetResponse(SerializableResponse):
    name: str
    cover_img: Optional[str]
    id: str
    # card_ids: List[str]

    def __init__(self, card_set: CardSet) -> None:
        super().__init__()
        self.name = card_set["name"]
        self.cover_img = card_set["cover_img"]
        self.id = str(card_set["_id"])
        # self.card_ids = [str(cid) for cid in card_set["card_ids"]]


class CardSetCollectionResponse(SerializableResponse):
    card_sets: Dict[str, Dict[str, Any]]

    def __init__(self, card_sets: DbCursor[CardSet]) -> None:
        super().__init__()
        self.card_sets = dict()
        for card_set in card_sets:
            self.card_sets[str(card_set["_id"])] = {
                "name": card_set["name"],
                "cover_img": card_set["cover_img"],
            }


class CreateCardSetResponse(SerializableResponse):
    set_id: str

    def __init__(self, id: ObjectId) -> None:
        super().__init__()
        self.set_id = str(id)
