from bson import ObjectId

from db.types.base import BaseDocument


class Flashcard(BaseDocument):
    q: str
    a: str
