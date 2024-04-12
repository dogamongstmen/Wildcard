from typing import Final, Generic, Optional, TypeVar, cast

from node import PrefixTreeNode
from structs.stack import Stack

WILDCARD: Final[str] = "**"

T = TypeVar("T")
Node = PrefixTreeNode[T]


class PrefixTree(Generic[T]):
    root: Node

    def __init__(self) -> None:
        self.root = PrefixTreeNode(None, False, None)

    def insert(self, key_str: str, value: T, wildcard: str = "*") -> None:
        current_node: Node = self.root

        for c in key_str:

            # Choose the key of the text node.
            key: str = WILDCARD if c == wildcard else c

            # Get the next node using the key.
            next_child: Optional[Node] = current_node.children.get(key)

            # We have to create a new node and then continue.
            if next_child == None:
                next_node: Node = PrefixTreeNode(None, False, current_node)
                current_node.children[key] = next_node
                current_node = next_node
            else:
                # Continue without creating a new node.
                current_node = cast(Node, next_child)

        current_node.value = value
        current_node.is_end = True

    def find(self, key_str: str) -> Optional[T]:
        current: Node = self.root

        for key in key_str:

            next_node: Optional[Node] = current.children.get(key)

            if next_node == None:

                wild_node: Optional[Node] = current.children.get(WILDCARD)
                if wild_node == None:
                    return None

                current = cast(Node, wild_node)
            else:
                current = cast(Node, next_node)

        return current.value

    def remove(self, key_str: str) -> None:

        key_history: Stack[str] = Stack(len(key_str))

        current: Node = self.root
        for key in key_str:
            next_node: Node = cast(Node, current.children.get(key))

            if next_node == None:
                wild_node: Node = cast(Node, current.children.get(WILDCARD))
                if wild_node == None:
                    return None
                else:
                    current = wild_node
                    key_history.push(WILDCARD)
            else:
                current = cast(Node, next_node)
                key_history.push(key)

        current.is_end = False
        current.value = None

        backtrack_node: Node = current
        while (
            backtrack_node.parent != None
            and len(backtrack_node.children) == 0
            and not backtrack_node.is_end
        ):

            backtrack_key: str = cast(str, key_history.pop())

            # print(
            #     [c_key for c_key in backtrack_node.children],
            #     f", children: {len(backtrack_node.children)}",
            #     f", end? {backtrack_node.is_end}",
            # )
            # print("\tKey: ", backtrack_key)

            del cast(Node, backtrack_node.parent).children[backtrack_key]

            backtrack_node = cast(Node, backtrack_node.parent)
