from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


# URL: "/"
def page_home_handler(
    state: ApplicationState, req: Request[None], res: Response
) -> None:
    res.html("<h1>Welcome home!</h1>")
