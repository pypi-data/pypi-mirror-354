from collections.abc import Callable, Iterator
from itertools import islice

from .splitter import Splitter


class SplitIter(Iterator[str]):
    """An iterator for splitting a string using a specified splitter."""

    def __init__(self, splitter: Splitter, text: str):
        self._splitter = splitter
        self._text = text
        self._start: int = 0
        self._end: int = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self._start > len(self._text):
            raise StopIteration
        _substr: str = self.__next_substr()
        return _substr

    def __next_substr(self) -> str:
        self._end, _cap = self._splitter.find(self._text, self._start)
        _substr = self._text[self._start : self._end]
        self._start = _cap
        return _substr


def make_iterator(
    splitter: Splitter, text: str, predicate: Callable[[str], bool] | None
) -> Iterator[str]:
    """Factory function to create a SplitIter instance."""

    it = SplitIter(splitter, text)
    if predicate:
        it = filter(predicate, it)
    if splitter.maxsplit >= 0:
        it = islice(it, splitter.maxsplit)
    return it
