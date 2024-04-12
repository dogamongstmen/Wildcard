from typing import Generic, List, Optional, TypeVar


T = TypeVar("T")


class Stack(Generic[T]):
    __stack: List[Optional[T]]
    capacity: int

    __pos: int

    def __init__(self, capacity: int) -> None:
        self.__stack = [None] * capacity
        self.capacity = capacity
        self.__pos = -1

    def push(self, value: T) -> None:

        if self.__pos == self.capacity - 1:
            return

        self.__pos += 1
        self.__stack[self.__pos] = value

    def pop(self) -> Optional[T]:
        if self.__pos == -1:
            return None
        popped: Optional[T] = self.__stack[self.__pos]
        self.__stack[self.__pos] = None
        self.__pos -= 1
        return popped

    def peek(self) -> Optional[T]:
        if self.__pos == -1:
            return None
        return self.__stack[self.__pos]

    def is_empty(self) -> bool:
        return self.__pos == -1
