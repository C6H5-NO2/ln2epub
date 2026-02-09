from abc import ABC, abstractmethod
from typing import final

from ..libxml.html import HtmlElement


class BaseRelinker(ABC):
    @final
    def relink(self, div: HtmlElement) -> dict[str, str]:
        # copy-pasted from `HtmlElement.rewrite_links`
        # https://github.com/lxml/lxml/blob/lxml-6.0.2/src/lxml/html/__init__.py#L601
        results: dict[str, str] = dict()
        for el, attrib, link, pos in div.iterlinks():
            new_link, file_path = self._replace_link(link=link, el=el, attrib=attrib, pos=pos)
            if new_link and file_path:
                results[new_link] = file_path
            if new_link == link:
                continue
            if new_link is None:
                if attrib is None:
                    el.text = ''
                else:
                    del el.attrib[attrib]
                continue

            if attrib is None:
                new = el.text[:pos] + new_link + el.text[pos + len(link):]
                el.text = new
            else:
                cur = el.get(attrib)
                if not pos and len(cur) == len(link):
                    new = new_link
                else:
                    new = cur[:pos] + new_link + cur[pos + len(link):]
                el.set(attrib, new)

        return results

    @abstractmethod
    def _replace_link(self, link: str, el: HtmlElement, attrib: str | None, pos: int) -> tuple[str | None, str | None]:
        """
        :param link: See `HtmlElement.iterlinks`.
        :return: A tuple of relinked link url and local file path, if any.
        """
        ...
