from typing import TypedDict
from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


class CardCollectionParams(TypedDict):
    collection_id: str


# Method: GET
# URL: /api/collections/:collection_id
def get_individual_col_handler(
    req: Request[ApplicationState, CardCollectionParams], res: Response
) -> None:
    res.html(f"<h1>Cards: {req.params['collection_id']}</h1>")


# Method: POST
# URL: /api/collections/:collection_id
def add_individual_col_handler(
    req: Request[ApplicationState, CardCollectionParams], res: Response
) -> None:
    # req._buffer
    res.status(400).json('{"message":"Added something."}')


# Method: DELETE
# URL: /api/collections/:collection_id
def delete_individual_col_handler(
    req: Request[ApplicationState, CardCollectionParams], res: Response
) -> None:
    # req._buffer
    res.status(400).json('{"message":"Added something."}')
