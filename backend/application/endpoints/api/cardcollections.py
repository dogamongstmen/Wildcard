from application.state import ApplicationState
from server.handling.request import Request
from server.handling.response import Response


# Method: GET
# URL: "/api/collections"
def get_col_handler(req: Request[ApplicationState, None], res: Response) -> None:
    res.html(
        """
             <ul>
             <li>Card collection 1</li>
             <li>Card collection 2</li>
             <li>...</li>
             <li>Card collection <i>n</i></li>
             </ul>
             """
    )


# Method: POST
# URL: "/api/collections"
def create_col_handler(
    req: Request[ApplicationState, None], res: Response
) -> None:
    # req._buffer
    res.status(400).json('{"message":"Added something."}')
