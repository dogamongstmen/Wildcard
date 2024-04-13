from typing import Dict, List, TypedDict, cast
from server.handling.request import Request
from server.handling.response import Response
from server.routing.route import Route
from structs.prefixtree.tree import PrefixTree
from server.routing.utils import route_path_to_trie_key, trie_route_search


class ProfileCommentParams(TypedDict):
    profile_id: str
    comment_id: str


def test_handler(req: Request[ProfileCommentParams], res: Response) -> None:
    print("Profile id: ", req.params.get("profile_id"))
    print("Comment id: ", req.params.get("comment_id"))


route_path: str = "/profile/:profile_id/comments/:comment_id"
trie: PrefixTree[Route] = PrefixTree()
trie.insert(route_path_to_trie_key(route_path), Route(route_path).get(test_handler))

param_list: List[str] = []
found: Route = cast(
    Route, trie_route_search(trie, "/profile/123/comments/456", out_params=param_list)
)

route_params: Dict[str, str] = found.populate_params(param_list)

found.handlers["GET"](Request(route_params), Response())
