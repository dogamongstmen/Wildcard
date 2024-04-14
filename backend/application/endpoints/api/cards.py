from typing import TypedDict

from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


class CardEndpointParams(TypedDict):
    card_id: str


# Method: GET
# URL: /api/cards/:card_id
def get_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.html(f"<h1>Card {req.params['card_id']}</h1>")


# Method: PATCH
# URL: /api/cards/:card_id
def update_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.html(f"<h1>Card {req.params['card_id']}, but different</h1>")


# Method: DELETE
# URL: /api/cards/:card_id
def remove_card_handler(
    req: Request[ApplicationState, CardEndpointParams], res: Response
) -> None:
    res.html(f"<h1>Goodbye {req.params['card_id']}</h1>")
