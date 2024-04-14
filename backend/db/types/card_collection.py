from typing import Dict, Generic, List, Optional, Union
from bson import ObjectId
from db.types.base import BaseDocument


class CardCollection(BaseDocument):
    name: str
    cover_img: Optional[str]
    card_ids: List[ObjectId]
    
