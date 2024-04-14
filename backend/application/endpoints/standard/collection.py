# URL: "/"
from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response

# URL: "/"
def home_handler(req: Request[ApplicationState, None], res: Response) -> None:
    res.html("<h1>Some card collection</h1>")