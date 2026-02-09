from typing import Protocol

from ..libxml.html import HtmlElement


class Relinker(Protocol):
    def relink(self, div: HtmlElement, /) -> dict[str, str]:
        """
        :param div: A normalised <div>. NB It will be modified in-place.
        :return: A mapping from relinked link url to local file path.
        """
        ...
