import re
from typing import Protocol

from ..libxml.html import HtmlElement


def is_valid_identifier(identifier: str | None) -> bool:
    if not identifier:
        return False
    if len(identifier) not in range(1, 256):
        return False
    return not not re.fullmatch(r'[\w\-]+', identifier, re.ASCII)


class Segmenter(Protocol):
    def segment(self, div: HtmlElement, /) -> dict[str, HtmlElement]:
        """
        :param div: A normalised <div>. NB It may be modified in-place.
        :return: A mapping from identifiers to <section>s.
        """
        ...
