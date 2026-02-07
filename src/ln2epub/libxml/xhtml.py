from io import Reader, Writer
from typing import Final, LiteralString

from lxml.builder import ElementMaker as _ElementMaker
from lxml.html import (
    XHTMLParser,
    html_to_xhtml as _html_to_xhtml,
    xhtml_parser as _lxml_xhtml_parser,
    xhtml_to_html as _xhtml_to_html,
)

from .html import HtmlElement, _html_parse
from .xml import ElementMaker, QName, XML_NAMESPACE, _xml_dump

XHTML_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/1999/xhtml'


def xhtml_element_maker(
    *,
    nsmap: dict[str, str] = None,
) -> ElementMaker[HtmlElement]:
    em = _ElementMaker(
        namespace=XHTML_NAMESPACE,
        nsmap=(nsmap if nsmap else {}) | {
            None: XHTML_NAMESPACE,
            'xml': XML_NAMESPACE,
        },
        makeelement=_lxml_xhtml_parser.makeelement,
    )
    return em


def xhtml_parse(fp: str | Reader[bytes], /) -> HtmlElement:
    return _html_parse(fp, parser=_xhtml_parser)


def xhtml_dump(el: HtmlElement, fp: str | Writer[bytes], /) -> None:
    _xml_dump(
        el,
        fp,
        method='xml',
        doctype='<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>',
    )


def html_to_xhtml(el: HtmlElement, /) -> None:
    _html_to_xhtml(el)


def xhtml_to_html(el: HtmlElement, /) -> None:
    _xhtml_to_html(el)


def xhtml_document(
    *body_children: HtmlElement,
    lang: str,
    title: str = '',
) -> HtmlElement:
    em = _xhtml_element_maker
    head: HtmlElement = em.head(em.title(title))
    body: HtmlElement = em.body(*body_children)
    html: HtmlElement = em.html(head, body)
    html.set(QName(XML_NAMESPACE, 'lang'), lang)
    return html


_xhtml_element_maker: Final[ElementMaker[HtmlElement]] = xhtml_element_maker()

_xhtml_parser: Final[XHTMLParser] = XHTMLParser(
    encoding='utf-8',
    no_network=True,
    huge_tree=False,
    remove_blank_text=False,
    remove_comments=True,
    remove_pis=True,
)
