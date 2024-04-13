from typing import List, Optional, TypeVar, cast

from structs.prefixtree.node import PrefixTreeNode
from structs.prefixtree.tree import WILDCARD, PrefixTree


def route_path_to_trie_key(route: str) -> str:
    key: str = "/"
    for sub in route.split("/"):
        if not sub.startswith(":"):
            key += sub
        else:
            key += "*"
    return key


# Maybe this should be in structs.prefixtree
T = TypeVar("T")


def trie_route_search(
    trie: PrefixTree[T], key_str: str, out_params: List[str]
) -> Optional[T]:

    current: PrefixTreeNode[T] = trie.root

    i: int = 0
    while i < len(key_str):
        key: str = key_str[i]

        next_node: PrefixTreeNode[T] = cast(
            PrefixTreeNode[T], current.children.get(key)
        )

        if next_node == None:
            wild_node = cast(PrefixTreeNode[T], current.children.get(WILDCARD))

            if wild_node == None:
                return None

            current = wild_node
            j: int = i + 1
            segment: str = ""
            while j < len(key_str) and key_str[j] != "/":
                segment += key_str[j]
                # Increment
                j += 1
            i = j
            out_params.append(segment)
        else:
            current = next_node

        # Increment
        i += 1

    return current.value
