import re
from typing import Protocol

from ..libxml.html import HtmlElement


def is_valid_identifier(identifier: str | None) -> bool:
    if not identifier:
        return False
    if len(identifier) not in range(1, 256):
        return False
    return not not re.fullmatch(r'[\w\-]+', identifier, re.ASCII)


class Sectioner(Protocol):
    def section(self, html: HtmlElement, /) -> dict[str, HtmlElement]:
        """
        :param html: An element where possible <section>s MUST only appear in the normalised <div>.
        :return: A mapping from identifiers to <section>s.
        """
        ...
