from typing import Protocol

from ..libxml.html import HtmlElement


class Relinker(Protocol):
    def relink(self, div: HtmlElement, /) -> dict[str, str]:
        """
        :param div: A normalised <div>. NB It will be modified in-place.
        :return: A mapping from dst url to src path of the linked files.
            `div` is modified with new links in-place.
        """
        ...
