from ..libxml.html import HtmlElement
from ..libxml.xhtml import XHTML_NAMESPACE
from ..libxml.xml import QName


class TagNameSelector:
    def __init__(self, tag: str):
        self._tag: str = tag

    def select_main(self, html: HtmlElement) -> HtmlElement:
        tag = self._tag
        el_iter = html.iter(tag, QName(XHTML_NAMESPACE, tag))
        el = next(el_iter, None)
        if el is None:
            raise ValueError(f'no match for tag name `{tag}`')
        return el
