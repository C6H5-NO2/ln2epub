from typing import Protocol

from ..libxml.html import HtmlElement


class Selector(Protocol):
    def select_main(self, html: HtmlElement, /) -> HtmlElement:
        """
        Selects the main content, not necessarily a <main>.
        """
        ...
