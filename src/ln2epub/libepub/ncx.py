import os.path
from dataclasses import dataclass
from functools import cache
from typing import Final, LiteralString

from .navigation_document import NavigationDocumentBuilder, NavigationItemBuilder
from ..libxml.xml import Element, ElementMaker, QName, XML_NAMESPACE, xml_element_maker
from ..util.frozenlist import frozenlist

NCX_NAMESPACE: Final[LiteralString] = 'http://www.daisy.org/z3986/2005/ncx/'


def ncx_element_maker() -> ElementMaker[Element]:
    return xml_element_maker(
        namespace=NCX_NAMESPACE,
        nsmap={
            None: NCX_NAMESPACE,
        }
    )


@cache
def _element_maker():
    return ncx_element_maker()


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NcxBuilder:
    nav_builder: NavigationDocumentBuilder
    dc_identifier: str
    xml_lang: str | None = None

    def build(self) -> Element:
        em = _element_maker()
        head = em.head(em.meta(content=self.dc_identifier, name='dtb:id'))
        doc_title = em.docTitle(em.text(self.nav_builder.heading))
        nav_map = self._build_nav_map(self.nav_builder.items)
        ncx = em.ncx(head, doc_title, nav_map, version='2005-1')
        if self.xml_lang:
            ncx.set(QName(XML_NAMESPACE, 'lang'), self.xml_lang)
        return ncx

    def _build_nav_map(self, items: frozenlist[NavigationItemBuilder]) -> Element:
        em = _element_maker()
        nav_map = em.navMap()
        for it in items:
            nav_point = self._build_nav_point(it)
            nav_map.append(nav_point)
        return nav_map

    def _build_nav_point(self, item: NavigationItemBuilder) -> Element:
        em = _element_maker()
        if not item.href:
            raise ValueError(item.text)
        nav_point = em.navPoint(
            em.navLabel(em.text(item.text)),
            em.content(src=item.href),
            id=os.path.basename(item.href),
        )
        if item.items:
            for it in item.items:
                sub_nav_point = self._build_nav_point(it)
                nav_point.append(sub_nav_point)
        return nav_point
