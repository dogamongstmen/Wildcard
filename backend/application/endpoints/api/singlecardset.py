from typing import TypedDict
from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


class CardSetParams(TypedDict):
    set_id: str


# Method: GET
# URL: /api/sets/:set_id
def get_single_card_set_handler(
    req: Request[ApplicationState, CardSetParams], res: Response
) -> None:
    res.html(f"<h1>Cards: {req.params['set_id']}</h1>")


# Method: POST
# URL: /api/sets/:set_id
def add_single_card_set_handler(
    req: Request[ApplicationState, CardSetParams], res: Response
) -> None:
    # req._buffer
    res.status(400).json('{"message":"Added something."}')


# Method: DELETE
# URL: /api/sets/:set_id
def delete_single_card_set_handler(
    req: Request[ApplicationState, CardSetParams], res: Response
) -> None:
    # req._buffer
    res.status(400).json('{"message":"Added something."}')
