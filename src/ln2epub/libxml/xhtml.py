from typing import Final

from .xml import Element, ElementMaker, QName, XML_NAMESPACE, _xml_dump

XHTML_NAMESPACE: Final[str] = 'http://www.w3.org/1999/xhtml'


def xhtml_element_maker() -> ElementMaker:
    return ElementMaker(
        namespace=XHTML_NAMESPACE,
        nsmap={
            None: XHTML_NAMESPACE,
            'xml': XML_NAMESPACE,
        },
    )


def xhtml_build(*, lang: str) -> Element:
    em = xhtml_element_maker()
    html: Element = em.html(em.head(em.title()), em.body())
    html.set(QName(XML_NAMESPACE, 'lang'), lang)
    return html


def xhtml_dump(el: Element, fp) -> None:
    _xml_dump(
        el,
        fp,
        doctype='<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n',
    )
