from dataclasses import dataclass
from functools import cache

from .content_document import EPUB_NAMESPACE, epub_xhtml_element_maker
from ..libxml.html import HtmlElement
from ..libxml.xml import QName
from ..util.frozenlist import frozenlist


@cache
def _element_maker():
    return epub_xhtml_element_maker()


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NavigationItemBuilder:
    text: str
    href: str | None = None
    items: frozenlist[NavigationItemBuilder] | None = None

    def _build_li(self) -> HtmlElement:
        em = _element_maker()
        li = em.li()

        if self.href:
            el = em.a(self.text, href=self.href)
        else:
            el = em.span(self.text)
        li.append(el)

        if self.items:
            sub_ol = em.ol()
            li.append(sub_ol)
            for it in self.items:
                sub_li = it._build_li()
                sub_ol.append(sub_li)
        else:
            li.text = ''

        return li


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NavigationDocumentBuilder:
    heading: str | None = None
    items: frozenlist[NavigationItemBuilder]

    def build(self) -> HtmlElement:
        """
        :return: <nav>
        """
        em = _element_maker()
        nav = em.nav()
        nav.set(QName(EPUB_NAMESPACE, 'type'), 'toc')
        if self.heading:
            h1 = em.h1(self.heading)
            nav.append(h1)
        ol = self._build_ol(self.items)
        nav.append(ol)
        return nav

    def _build_ol(self, items: frozenlist[NavigationItemBuilder]) -> HtmlElement:
        em = _element_maker()
        ol = em.ol()
        for it in items:
            li = it._build_li()
            ol.append(li)
        return ol
