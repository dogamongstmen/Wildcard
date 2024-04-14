from typing import List, Optional
from bson import ObjectId
from db.types.base import BaseDocument


class CardSet(BaseDocument):
    name: str
    cover_img: Optional[str]
    card_ids: List[ObjectId]
