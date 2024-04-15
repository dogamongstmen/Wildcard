import json
import logging
import traceback
from bson import ObjectId
from application.routes.api.endpoints.singlecardset.root import CardSetParams
from application.routes.api.responsetypes.errors.errors import (
    FieldErrorResponse,
    InternalServerErrorResponse,
    MalformedRequestErrorResponse,
    NotFoundErrorResponse,
)
from application.routes.api.responsetypes.standard.flashcard import FlashcardResponse
from application.state import ApplicationState
from db.collections import COLLECTION_CARDS
from db.types.card import Flashcard, read_flashcard, update_flashcard
from server.handling.request import Request
from server.handling.response import Response


from pymongo.collection import Collection


class SingleCardParams(CardSetParams):
    card_id: str


# Methods: GET, PATCH, DELETE
# URL: /api/card_sets/:set_id/cards/:card_id
def get_single_card_handler(
    state: ApplicationState, req: Request[SingleCardParams], res: Response
) -> None:

    try:

        if not ObjectId.is_valid(req.params["set_id"]):
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return
        if not ObjectId.is_valid(req.params["card_id"]):
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        card_col: Collection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        query_result: Flashcard = read_flashcard(
            card_col, ObjectId(req.params["set_id"]), ObjectId(req.params["card_id"])
        )

        if query_result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        res.json(FlashcardResponse(query_result).to_serializable())

    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


def update_single_card_handler(
    state: ApplicationState, req: Request[SingleCardParams], res: Response
) -> None:
    try:

        body: Flashcard = json.loads(
            req._buffer.read(int(req.headers["content-length"]))
        )

        if body.get("q") == None and body.get("a") == None:
            res.status(400).json(FieldErrorResponse("q & a").to_serializable())
            return

        if not ObjectId.is_valid(req.params["set_id"]):
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card set does not exist."
                ).to_serializable()
            )
            return

        if not ObjectId.is_valid(req.params["card_id"]):
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        card_col: Collection[Flashcard] = state.card_data_db.get_collection(
            COLLECTION_CARDS
        )

        result: Flashcard = update_flashcard(
            card_col,
            ObjectId(req.params["set_id"]),
            ObjectId(req.params["card_id"]),
            body,
        )
        if result == None:
            res.status(404).json(
                NotFoundErrorResponse(
                    "The requested card does not exist."
                ).to_serializable()
            )
            return

        res.json(FlashcardResponse(result).to_serializable())

    except json.JSONDecodeError:
        res.status(400).json(MalformedRequestErrorResponse().to_serializable())
    except Exception:
        res.status(500).json(InternalServerErrorResponse().to_serializable())
        logging.error(traceback.format_exc())


def delete_single_card_handler(
    state: ApplicationState, req: Request[SingleCardParams], res: Response
) -> None: ...
