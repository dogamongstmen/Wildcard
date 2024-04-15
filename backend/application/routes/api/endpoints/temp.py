import json
import logging
import traceback
from typing import Dict, Optional, TypedDict, cast

from bson import ObjectId
from pymongo import ReturnDocument

from application.routes.api.responsetypes.errors.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
    NotFoundErrorResponse,
)
from application.routes.api.responsetypes.standard.flashcard import FlashcardResponse
from application.state import ApplicationState
from db.collections import COLLECTION_CARDS
from db.types.card import Flashcard
from server.handling.request import Request
from server.handling.response import Response

from pymongo.collection import Collection

from bson.errors import InvalidId


class CardEndpointParams(TypedDict):
    card_id: str

# Method: GET
# URL: /api/cards/:card_id
def api_get_card_handler(
    state: ApplicationState, req: Request[CardEndpointParams], res: Response
) -> None:

    try:

        cards_col: Collection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        result: Optional[Flashcard] = cards_col.find_one(
            {"_id": ObjectId(req.params["card_id"])}
        )

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        # We do this to appease the type checker.
        result = cast(Flashcard, result)

        res.json(FlashcardResponse(result).to_serializable())

    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card does not exist."
            ).to_serializable()
        )
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


# Method: PATCH
# URL: /api/cards/:card_id
def api_update_card_handler(
    state: ApplicationState, req: Request[CardEndpointParams], res: Response
) -> None:

    try:

        body: Flashcard = json.loads(
            req._buffer.read(int(req.headers["content-length"]))
        )

        if body.get("q") == None and body.get("a") == None:
            res.status(400).json(FieldErrorResponse("q & a").to_serializable())
            return

        cards_col: Collection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        to_insert: Dict[str, str] = dict()
        if body.get("q") != None:
            to_insert["q"] = body["q"]
        if body.get("a") != None:
            to_insert["a"] = body["a"]

        result: Optional[Flashcard] = cards_col.find_one_and_update(
            {"_id": ObjectId(req.params["card_id"])},
            {"$set": to_insert},
            return_document=ReturnDocument.AFTER,
        )

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        # We do this to appease the type checker.
        result = cast(Flashcard, result)

        res.json(FlashcardResponse(result).to_serializable())

    except TypeError:
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
# URL: /api/cards/:card_id
def api_remove_card_handler(
    state: ApplicationState, req: Request[CardEndpointParams], res: Response
) -> None:
    try:

        cards_col: Collection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        result: Optional[Flashcard] = cards_col.find_one_and_delete(
            {"_id": ObjectId(req.params["card_id"])}
        )

        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        # We do this to appease the type checker.
        result = cast(Flashcard, result)

        res.json(FlashcardResponse(result).to_serializable())

    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card does not exist."
            ).to_serializable()
        )
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
