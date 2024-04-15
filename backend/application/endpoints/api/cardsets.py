import json
from application.endpoints.api.types.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
)
from application.endpoints.api.types.responses.cardset import CardSetCollectionResponse
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.types.cardset import CardSet
from server.handling.request import Request
from server.handling.response import Response

from pymongo.collection import Collection, InsertOneResult

import logging
import traceback


# Method: GET
# URL: /api/sets
def api_get_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:

    card_set_collection: Collection[CardSet] = state.card_data_db.get_collection(
        COLLECTION_CARD_SETS
    )

    res.json(CardSetCollectionResponse(card_set_collection.find()).to_serializable())


# Method: POST
# URL: /api/sets
def api_create_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:
    try:
        body: CardSet = json.loads(req._buffer.read(int(req.headers["content-length"])))

        if body.get("name") == None:
            res.status(400).json(FieldErrorResponse("name").to_serializable())
            return

        card_set_collection: Collection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        insert_data: CardSet = {  # type: ignore
            "name": body["name"],
            "cover_img": None,
            "card_ids": [],
        }

        result: InsertOneResult = card_set_collection.insert_one(insert_data)

        res.json({"set_id": str(result.inserted_id)})

    except TypeError:
        res.status(400).json(MalformedRequestErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
