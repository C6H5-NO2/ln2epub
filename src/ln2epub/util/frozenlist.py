from collections.abc import Iterator
from typing import Protocol, overload


class frozenlist[_T](Protocol):
    def copy(self) -> frozenlist[_T]:
        ...

    def index(self, value: _T, start: int = 0, stop: int = ..., /) -> int:
        ...

    def count(self, value: _T, /) -> int:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[_T]:
        ...

    @overload
    def __getitem__(self, index: int, /) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice, /) -> frozenlist[_T]:
        ...

    def __contains__(self, value: _T, /) -> bool:
        ...

    def __reversed__(self) -> Iterator[_T]:
        ...
