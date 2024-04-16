from typing import Dict, cast
from bson import ObjectId
from pymongo import ReturnDocument

from db.types.base import BaseDocument

from pymongo.collection import Collection


class Flashcard(BaseDocument):
    parent_id: ObjectId
    q: str
    a: str


def read_flashcard(
    col: Collection[Flashcard], set_id: ObjectId, card_id: ObjectId
) -> Flashcard:
    return cast(Flashcard, col.find_one({"_id": card_id, "parent_id": set_id}))


def update_flashcard(
    col: Collection[Flashcard], set_id: ObjectId, card_id: ObjectId, new: Flashcard
) -> Flashcard:

    update: Dict[str, str] = dict()
    if new["q"] != None:
        update["q"] = new["q"]
    if new["a"] != None:
        update["a"] = new["a"]

    return col.find_one_and_update(
        {"_id": card_id, "parent_id": set_id},
        {"$set": update},
        return_document=ReturnDocument.AFTER,
    )


def delete_flashcard(
    col: Collection[Flashcard], set_id: ObjectId, card_id: ObjectId
) -> Flashcard:
    return col.find_one_and_delete({"_id": card_id, "parent_id": set_id})
