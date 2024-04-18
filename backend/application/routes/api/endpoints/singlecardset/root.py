from typing import TypedDict
import json
import logging
import traceback
from typing import TypedDict

from bson import ObjectId
from bson.errors import InvalidId
from application.responses.api.errors.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
    NotFoundErrorResponse,
)
from application.responses.api.standard.cardset import CardSetResponse
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.db import DbCollection
from db.types.cardset import (
    CardSet,
    delete_card_set_by_id,
    read_card_set_by_id,
    update_card_set_by_id,
)
from server.handling.request import Request
from server.handling.response import Response


class CardSetParams(TypedDict):
    set_id: str


# Method: GET
# URL: /api/card_sets/:set_id
def api_get_single_card_set_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
) -> None:

    try:
        set_col: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        result: CardSet = read_card_set_by_id(set_col, ObjectId(req.params["set_id"]))

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return

        res.json(CardSetResponse(result).to_serializable())

    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card set does not exist."
            ).to_serializable()
        )
        logging.error(traceback.format_exc())
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


# Method: PATCH
# URL: /api/card_sets/:set_id
def api_update_single_card_set_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
) -> None:

    try:

        body: CardSet = json.loads(req._buffer.read(int(req.headers["content-length"])))

        if body.get("name") == None:
            res.status(400).json(FieldErrorResponse("name").to_serializable())
            return

        set_col: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        result: CardSet = update_card_set_by_id(
            set_col, ObjectId(req.params["set_id"]), body["name"]
        )

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        res.json(CardSetResponse(result).to_serializable())

    except json.JSONDecodeError:
        res.status(400).json(MalformedRequestErrorResponse().to_serializable())
    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card does not exist."
            ).to_serializable()
        )
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


# Method: DELETE
# URL: /api/card_sets/:set_id
def api_delete_single_card_set_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
) -> None:

    try:
        set_col: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        result: CardSet = delete_card_set_by_id(set_col, ObjectId(req.params["set_id"]))

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return

        res.json(CardSetResponse(result).to_serializable())

    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card set does not exist."
            ).to_serializable()
        ) 
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
