from typing import Protocol

from ..libxml.html import HtmlElement


class Sectioner(Protocol):
    def section(self, html: HtmlElement, /) -> dict[str, HtmlElement]:
        """
        :param html: An element where possible <section>s MUST only appear in the normalised <div>.
        :return: A mapping from identifiers to <section>s.
        """
        ...
