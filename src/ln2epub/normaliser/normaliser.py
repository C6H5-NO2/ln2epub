from typing import Protocol

from ..libxml.html import HtmlElement


class Normaliser(Protocol):
    def select_main(self, html: HtmlElement, /) -> HtmlElement:
        ...

    def normalise(self, main: HtmlElement, /) -> HtmlElement:
        ...
