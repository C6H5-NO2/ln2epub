from dataclasses import dataclass

from .content_document import EPUB_NAMESPACE, epub_xhtml_element_maker
from ..libxml.xml import Element, ElementMaker, QName


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NavigationItemBuilder:
    text: str
    href: str = None
    items: list[NavigationItemBuilder] = None


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NavigationDocumentBuilder:
    heading: str = None
    items: list[NavigationItemBuilder]


def build_navigation_document(arg: NavigationDocumentBuilder) -> Element:
    em = epub_xhtml_element_maker()
    nav: Element = em.nav()
    nav.set(QName(EPUB_NAMESPACE, 'type'), 'toc')
    if arg.heading:
        h1 = em.h1(arg.heading)
        nav.append(h1)
    ol = _build_ol(arg.items, em)
    nav.append(ol)
    return nav


def _build_ol(items: list[NavigationItemBuilder], em: ElementMaker) -> Element:
    ol: Element = em.ol()
    for item in items:
        li: Element = em.li()
        ol.append(li)
        if item.href:
            el = em.a(item.text, href=item.href)
        else:
            el = em.span(item.text)
        li.append(el)
        if item.items:
            sub_ol = _build_ol(item.items, em)
            li.append(sub_ol)
    return ol
