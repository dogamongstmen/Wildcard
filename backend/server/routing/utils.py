from typing import List, Optional, TypeVar, cast

from structs.prefixtree.node import PrefixTreeNode
from structs.prefixtree.tree import WILDCARD, PrefixTree


def route_path_to_trie_key(route: str) -> str:
    key: str = ""

    i: int = 0
    while i < len(route):
        sub: str = route[i]

        if sub == ":":
            j: int = i + 1
            while j < len(route) and route[j] != "/":
                j += 1
            i = j
            key += "*"
        else:
            key += sub

        # Inc
        i += 1

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
            # print("\t", key)

            wild_node = cast(PrefixTreeNode[T], current.children.get(WILDCARD))

            if wild_node == None:
                return None

            current = wild_node
            j: int = i + 1
            segment: str = key
            while j < len(key_str) and key_str[j] != "/":
                segment += key_str[j]
                # Increment
                j += 1
            i = j
            # print(segment)
            out_params.append(segment)
        else:
            # print(key)
            current = next_node

        # Increment
        i += 1

    print("\n")
    return current.value
