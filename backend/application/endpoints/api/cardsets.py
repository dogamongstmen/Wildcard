import json
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.types.cardset import CardSet
from server.handling.request import Request
from server.handling.response import Response

from pymongo.collection import Collection


# Method: GET
# URL: /api/sets
def api_get_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:

    card_set_collection: Collection[CardSet] = state.card_data_db.get_collection(
        COLLECTION_CARD_SETS
    )

    res.json(
        json.dumps(
            {
                "sets": [
                    {
                        "name": card_set["name"],
                        "cover_img": card_set["cover_img"],
                        "card_ids": [
                            str(c_object_id) for c_object_id in card_set["card_ids"]
                        ],
                    }
                    for card_set in card_set_collection.find()
                ]
            }
        )
    )


# Method: POST
# URL: /api/sets
def api_create_card_set_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:
    # req._buffer
    res.json(json.dumps({"message": "Added card"}))
