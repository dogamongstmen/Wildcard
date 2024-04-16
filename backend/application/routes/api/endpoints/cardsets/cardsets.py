import json
from application.routes.api.responsetypes.errors.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
)
from application.routes.api.responsetypes.standard.cardset import (
    CardSetCollectionResponse,
    CreateCardSetResponse,
)
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.db import DbCollection, InsertOneResult
from db.types.cardset import CardSet
from server.handling.request import Request
from server.handling.response import Response

import logging
import traceback


# Method: GET
# URL: /api/card_sets
def api_get_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:

    card_set_collection: DbCollection[CardSet] = state.card_data_db.get_collection(
        COLLECTION_CARD_SETS
    )

    res.json(CardSetCollectionResponse(card_set_collection.find()).to_serializable())


# Method: POST
# URL: /api/card_sets
def api_create_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:
    try:
        body: CardSet = json.loads(req._buffer.read(int(req.headers["content-length"])))

        if body.get("name") == None:
            res.status(400).json(FieldErrorResponse("name").to_serializable())
            return

        card_set_collection: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        insert_data: CardSet = {  # type: ignore
            "name": body["name"],
            "cover_img": None,
            "card_ids": [],
        }

        result: InsertOneResult = card_set_collection.insert_one(insert_data)

        res.json(CreateCardSetResponse(result.inserted_id).to_serializable())

    except json.JSONDecodeError:
        res.status(400).json(MalformedRequestErrorResponse().to_serializable())
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
