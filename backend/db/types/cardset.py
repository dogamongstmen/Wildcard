from typing import Optional, cast
from bson import ObjectId
from pymongo import ReturnDocument
from db.types.base import BaseDocument

from pymongo.collection import Collection


class CardSet(BaseDocument):
    name: str
    cover_img: Optional[str]


def read_card_set_by_id(col: Collection[CardSet], id: ObjectId) -> CardSet:
    return cast(CardSet, col.find_one({"_id": id}))


def update_card_set_by_id(
    col: Collection[CardSet], id: ObjectId, new_name: str
) -> CardSet:
    return col.find_one_and_update(
        {"_id": id},
        {"$set": {"name": new_name}},
        return_document=ReturnDocument.AFTER,
    )


def delete_card_set_by_id(col: Collection[CardSet], id: ObjectId) -> CardSet:
    return cast(CardSet, col.find_one_and_delete({"_id": ObjectId(id)}))
