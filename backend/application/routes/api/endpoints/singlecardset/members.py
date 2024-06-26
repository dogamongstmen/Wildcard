import json
import logging
import traceback

from bson import ObjectId
from application.responses.api.errors.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
    NotFoundErrorResponse,
)
from application.responses.api.standard.cardset import CardSetMembersResponse
from application.responses.api.standard.flashcard import CreatedFlashcardResponse
from application.routes.api.endpoints.singlecardset.root import CardSetParams
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS, COLLECTION_CARDS
from db.db import DbCollection, DbCursor, InsertOneResult
from db.types.card import Flashcard
from db.types.cardset import CardSet, read_card_set_by_id
from server.handling.request import Request
from server.handling.response import Response

from bson.errors import InvalidId


# Method: GET
# URL: /api/card_sets/:set_id/cards
def api_get_card_set_members_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
):
    try:

        set_col: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        cards_col: DbCollection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        set_id: ObjectId = ObjectId(req.params["set_id"])

        find_set_result: CardSet = read_card_set_by_id(set_col, set_id)

        if find_set_result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return

        found_cards: DbCursor[Flashcard] = cards_col.find({"parent_id": set_id})

        resbody = CardSetMembersResponse(found_cards)

        res.json(resbody.to_serializable())

    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card set does not exist."
            ).to_serializable()
        )
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


# Method: POST
# URL: /api/card_sets/:set_id/cards
def api_create_card_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
):
    try:

        body: Flashcard = json.loads(
            req._buffer.read(int(req.headers["content-length"]))
        )

        if body.get("q") == None or body.get("a") == None:
            res.status(400).json(FieldErrorResponse("q | a").to_serializable())
            return

        set_id: ObjectId = ObjectId(req.params["set_id"])

        set_col: DbCollection[CardSet] = state.card_data_db.get_collection(
            COLLECTION_CARD_SETS
        )

        find_set_result: CardSet = read_card_set_by_id(set_col, set_id)
        if find_set_result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return

        cards_col: DbCollection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        to_insert: Flashcard = {  # type: ignore
            "q": body["q"],
            "a": body["a"],
            "parent_id": set_id,
        }
        create_result: InsertOneResult = cards_col.insert_one(to_insert)

        res.json(CreatedFlashcardResponse(create_result.inserted_id).to_serializable())

    except json.JSONDecodeError:
        res.status(400).json(MalformedRequestErrorResponse().to_serializable())
    except InvalidId:
        res.status(404).json(
            NotFoundErrorResponse(
                "The requested card set does not exist."
            ).to_serializable()
        )
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())
