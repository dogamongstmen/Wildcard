from bson import ObjectId

from db.types.base import BaseDocument


class Flashcard(BaseDocument):
    parent_id: ObjectId
    q: str
    a: str
