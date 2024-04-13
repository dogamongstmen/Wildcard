from http.server import BaseHTTPRequestHandler
from os import system
from socketserver import BaseRequestHandler
from typing import Dict, List, TypedDict, cast
from server.handling.request import Request
from server.handling.response import Response
from server.routing.route import Route
from server.serve.basehandler import ExtendedHTTPRequestHandler
from server.serve.baseserver import BaseServer
from structs.prefixtree.tree import PrefixTree
from server.routing.utils import route_path_to_trie_key, trie_route_search


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


def cart_handler(req: Request[List[str], None], res: Response) -> None:
    print("Fruits in my shopping cart: ", req.state)

    cart: str = "".join([f"<li>{fruit}</li>" for fruit in req.state])
    res.html(
        f"""<h1>Shopping cart:</h1>
             <ul>
             {cart}
             </ul>"""
    )


def main() -> None:
    # system("clear")

    routes: PrefixTree[Route] = PrefixTree()

    routes.insert(route_path_to_trie_key("/cart"), Route("/cart").get(cart_handler))

    routes.insert(
        route_path_to_trie_key("/profile/:profile_id"),
        Route("/profile/:profile_id").get(base_profile_handler),
    )

    routes.insert(
        route_path_to_trie_key("/profile/:profile_id/comments"),
        Route("/profile/:profile_id/comments").get(profile_comments_handler),
    )

    routes.insert(
        route_path_to_trie_key("/profile/:profile_id/comments/:comment_id"),
        Route("/profile/:profile_id/comments/:comment_id").get(
            profile_single_comment_handler
        ),
    )

    test_state: List[str] = ["🍇", "🍉", "🍊", "🍌", "🥭", "🫐", "🍎"]
    httpd: BaseServer[List[str]] = BaseServer(
        ("", 5000), ExtendedHTTPRequestHandler, routes, test_state
    )
    httpd.serve_forever()


main()
