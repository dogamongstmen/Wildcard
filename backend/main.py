from typing import List
from structs.prefixtree.tree import PrefixTree
from server.routing.utils import route_path_to_trie_key, trie_route_search

trie: PrefixTree[str] = PrefixTree()

base_profile_key: str = route_path_to_trie_key(
    "/profile/:profile_id/comments/:comments_id"
)

trie.insert(base_profile_key, "Base profile page")

param_list: List[str] = []
print(trie_route_search(trie, "/profile/dasdadasdasdasdasd/comments/jjjjjjj", out_params=param_list))
print(param_list)
