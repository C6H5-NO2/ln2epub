from typing import Protocol

from ..libxml.html import HtmlElement


class Normaliser(Protocol):
    def normalise(self, main: HtmlElement, /) -> HtmlElement:
        """
        :return: MUST be a <div> without text or tail or any attrib
            whose direct children MUST be <div>, <h1>-<h6>, <section>,
            <span>, or <p>, all without tail.
        """
        ...
