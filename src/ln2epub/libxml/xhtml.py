from functools import cache
from typing import Final, LiteralString

from lxml.html import xhtml_parser

from .html import HtmlElement
from .xml import Element, ElementMaker, QName, XML_NAMESPACE, _xml_dump

XHTML_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/1999/xhtml'


def xhtml_element_maker(
    *,
    nsmap: dict[str, str] = None,
) -> ElementMaker:
    em = ElementMaker(
        namespace=XHTML_NAMESPACE,
        nsmap=(nsmap if nsmap else {}) | {
            None: XHTML_NAMESPACE,
            'xml': XML_NAMESPACE,
        },
        makeelement=xhtml_parser.makeelement,
    )
    return em


@cache
def _element_maker() -> ElementMaker:
    return xhtml_element_maker()


def xhtml_document(
    *body_children: HtmlElement,
    lang: str,
    title: str = '',
) -> HtmlElement:
    em = _element_maker()
    head: HtmlElement = em.head(em.title(title))
    body: HtmlElement = em.body(*body_children)
    html: HtmlElement = em.html(head, body)
    html.set(QName(XML_NAMESPACE, 'lang'), lang)
    return html


def xhtml_dump(el: Element, fp) -> None:
    _xml_dump(
        el,
        fp,
        doctype='<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>',
    )
