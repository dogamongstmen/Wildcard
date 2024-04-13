from threading import Thread
from typing import List, Optional, TypedDict, cast
from server.handling.request import Request
from server.handling.response import Response
from server.routing.route import Route
from server.server import Server, Socket


class BaseProfileParams(TypedDict):
    profile_id: str


def base_profile_handler(
    req: Request[List[str], BaseProfileParams], res: Response
) -> None:
    # print("Profile id: ", req.params.get("profile_id"))
    res.html(f'<h1>Profile: {req.params.get("profile_id")}</h1>')


def profile_comments_handler(
    req: Request[List[str], BaseProfileParams], res: Response
) -> None:
    # print("Profile id: ", req.params.get("profile_id"))
    res.html(
        f"""<h1>Profile: {req.params.get("profile_id")}</h1>
             <ul>
             <li>1</l1>
             <li>2</l1>
             <li>...</l1>
             <li>n</l1>
             </ul>"""
    )


class ProfileCommentParams(TypedDict):
    profile_id: str
    comment_id: str


def profile_single_comment_handler(
    req: Request[List[str], ProfileCommentParams], res: Response
) -> None:
    # print("Profile id: ", req.params.get("profile_id"))
    res.html(f'<h1>{req.params.get("profile_id")}->{req.params.get("comment_id")}</h1>')


def main() -> None:

    fruits: List[str] = ["🍇", "🍉", "🍊", "🍌", "🥭", "🫐", "🍎"]
    server: Server[List[str]] = Server(fruits)

    server.route(Route("/profile/:profile_id").get(base_profile_handler))
    server.route(Route("/profile/:profile_id/comments").get(profile_comments_handler))
    server.route(
        Route("/profile/:profile_id/comments/:comment_id").get(
            profile_single_comment_handler
        )
    )

    socket: Optional[Socket] = server.listen("", 5000)

    # Block the main thread.
    cast(Thread, server._listening_thread).join()


main()
