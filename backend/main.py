from typing import cast
from pymongo import MongoClient

from db.collections import COLLECTION_CARD_COLLECTIONS
from db.credentials import get_db_credentials
from db.databases import DB_FLASHCARD_DATA
from db.types.card_collection import CardCollection


def main() -> None:

    credentials: str = get_db_credentials()
    db_client: MongoClient = MongoClient(credentials)

    db = db_client[DB_FLASHCARD_DATA]

    col = db.get_collection(COLLECTION_CARD_COLLECTIONS)

    card_sets = col.find()
    for _card_col in card_sets:
        card_col: CardCollection = cast(CardCollection, _card_col)

        id_bin: bytes = card_col["_id"].binary

        print(id_bin[0:4].hex())
        print(id_bin[4:9].hex())
        print(id_bin[9:12].hex(), "\n")

        print(id_bin.hex())

    db_client.close()


main()
