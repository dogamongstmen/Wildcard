import json
from typing import TypedDict

from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


class CardEndpointParams(TypedDict):
    card_id: str


# Method: GET
# URL: /api/cards/:card_id
def api_get_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.json(json.dumps({"message": f"This is card {req.params['card_id']}"}))


# Method: PATCH
# URL: /api/cards/:card_id
def api_update_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.json(json.dumps({"message": f"Changed card {req.params['card_id']}"}))


# Method: DELETE
# URL: /api/cards/:card_id
def api_remove_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.json(json.dumps({"message": f"Goodbye, card {req.params['card_id']}"}))
