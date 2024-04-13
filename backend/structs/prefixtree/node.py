from typing import Dict, Generic, Optional, Self, TypeVar


T = TypeVar("T")


class PrefixTreeNode(Generic[T]):

    value: Optional[T]
    children: Dict[str, Self]
    is_end: bool
    parent: Optional[Self]

    def __init__(
        self,
        value: Optional[T] = None,
        is_end: bool = False,
        parent: Optional[Self] = None,
    ) -> None:
        self.value = value
        self.is_end = is_end
        self.children = dict()
        self.parent = parent
