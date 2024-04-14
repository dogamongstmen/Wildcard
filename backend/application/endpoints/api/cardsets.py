import json
from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


# Method: GET
# URL: /api/sets
def api_get_card_set_handler(
    req: Request[ApplicationState, None], res: Response
) -> None:
    res.json(
        json.dumps({"sets": [{"id": "1"}, {"id": "2"}, {"id": "..."}, {"id": "n"}]})
    )


# Method: POST
# URL: /api/sets
def api_create_card_set_handler(
    req: Request[ApplicationState, None], res: Response
) -> None:
    # req._buffer
    res.json(json.dumps({"message": "Added card"}))
