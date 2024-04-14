import json
from application.state import ApplicationState
from db.collections import COLLECTION_CARD_SETS
from db.types.cardset import CardSet
from server.handling.request import Request
from server.handling.response import Response

from pymongo.collection import Collection, InsertOneResult


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
    try:
        body: CardSet = json.loads(req._buffer.read(int(req.headers["content-length"])))

        if body["name"] == None:
            res.status(400).json(
                '{"error":"Request body must contain a `name` field."}'
            )
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

        print(result)

        res.json(json.dumps({"set_id": str(result.inserted_id)}))
    except:
        res.status(400).json('{"error": "Malformed request data."}')
