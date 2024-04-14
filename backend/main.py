from typing import cast
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from db.collections import COLLECTION_CARD_SETS
from db.credentials import get_db_credentials
from db.databases import DB_FLASHCARD_DATA
from db.types.cardset import CardSet


def main() -> None:

    credentials: str = get_db_credentials()
    db_client: MongoClient = MongoClient(credentials)

    db: Database = db_client.get_database(DB_FLASHCARD_DATA)
    col: Collection[CardSet] = db.get_collection(COLLECTION_CARD_SETS)

    card_sets: Cursor[CardSet] = col.find()
    for card_col in card_sets:

        id_bin: bytes = card_col["_id"].binary

        print(id_bin[0:4].hex())
        print(id_bin[4:9].hex())
        print(id_bin[9:12].hex(), "\n")

        print(id_bin.hex())

    db_client.close()


main()
