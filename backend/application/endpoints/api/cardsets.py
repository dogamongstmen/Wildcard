import json
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.databases import DB_FLASHCARD_DATA
from db.types.cardset import CardSet
from server.handling.request import Request
from server.handling.response import Response

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor


# Method: GET
# URL: /api/sets
def api_get_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:

    db: Database = state.db_client.get_database(DB_FLASHCARD_DATA)
    col: Collection[CardSet] = db.get_collection(COLLECTION_CARD_SETS)

    card_sets: Cursor[CardSet] = col.find()
    for card_col in card_sets:

        id_bin: bytes = card_col["_id"].binary

        print(id_bin[0:4].hex())
        print(id_bin[4:9].hex())
        print(id_bin[9:12].hex(), "\n")

        print(id_bin.hex())

    res.json(
        json.dumps({"sets": [{"id": "1"}, {"id": "2"}, {"id": "..."}, {"id": "n"}]})
    )


# Method: POST
# URL: /api/sets
def api_create_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:
    # req._buffer
    res.json(json.dumps({"message": "Added card"}))
