from typing import TypedDict
from bson import ObjectId


class BaseDocument(TypedDict):
    _id: ObjectId
