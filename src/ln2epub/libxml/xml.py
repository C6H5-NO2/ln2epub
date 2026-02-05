from typing import Final, LiteralString, Protocol

from lxml.builder import ElementMaker as _ElementMaker
from lxml.etree import Element as makeelement, ElementTree, QName as _QName, _Element, _ElementTree

XML_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/XML/1998/namespace'
XMLNS_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/2000/xmlns/'

QName = _QName

type Element = _Element


class _ElementMakerCaller[E: Element = Element](Protocol):
    def __call__(self, *children: str | Element, **attrib: str) -> E:
        ...


class ElementMaker[E: Element = Element](Protocol):
    def __call__(self, tag: str | QName, *children: str | Element, **attrib: str) -> E:
        ...

    def __getattr__(self, tag: str) -> _ElementMakerCaller[E]:
        ...


def xml_element_maker(
    *,
    namespace: str = None,
    nsmap: dict[str | None, str] = None,
) -> ElementMaker[Element]:
    # em = lxml.builder.E
    em = _ElementMaker(
        namespace=namespace,
        nsmap=nsmap,
        makeelement=makeelement,
    )
    return em


def xml_dump(el: Element, fp) -> None:
    _xml_dump(el, fp)


def _xml_dump(
    el: Element,
    fp,
    *,
    doctype: str | None = '<?xml version="1.0" encoding="utf-8"?>',
) -> None:
    if not hasattr(fp, 'write'):
        with open(fp, 'wb') as fp:
            _xml_dump(el, fp, doctype=doctype)
        return
    et: _ElementTree = ElementTree(el)
    et.write(
        fp,
        encoding='utf-8',
        method='xml',
        pretty_print=True,
        xml_declaration=False,
        with_tail=False,
        doctype=doctype,
    )


def get_text_tail(el: Element, /) -> str | None:
    return el[-1].tail if len(el) else el.text


def set_text_tail(el: Element, text_tail: str | None, /) -> None:
    if len(el):
        el[-1].tail = text_tail
    else:
        el.text = text_tail


def unwrap_sole_child[E: Element](el: E | None, /) -> E | None:
    if el is None:
        return None
    if len(el) != 1:
        return None
    if el.text or el[0].tail:
        return None
    return el[0]
