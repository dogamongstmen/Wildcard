from typing import TypedDict
from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


class CardSetParams(TypedDict):
    set_id: str


# URL: "/collections/:set_id"
def page_get_card_set_handler(
    state: ApplicationState, req: Request[CardSetParams], res: Response
) -> None:
    res.html(f"<h1>Card collection: {req.params['set_id']}</h1>")
