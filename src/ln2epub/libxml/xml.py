from typing import Final

import lxml.builder
import lxml.etree

XML_NAMESPACE: Final[str] = 'http://www.w3.org/XML/1998/namespace'

# noinspection PyProtectedMember
Element = lxml.etree._Element
ElementFactory = lxml.etree.Element
ElementMaker = lxml.builder.ElementMaker
# noinspection PyProtectedMember
ElementTree = lxml.etree._ElementTree
ElementTreeFactory = lxml.etree.ElementTree
QName = lxml.etree.QName


def xml_dump(el: Element, fp) -> None:
    _xml_dump(el, fp)


def _xml_dump(el, fp, *, doctype='<?xml version="1.0" encoding="utf-8"?>') -> None:
    if not hasattr(fp, 'write'):
        with open(fp, 'wb') as fp:
            _xml_dump(el, fp, doctype=doctype)
        return
    # noinspection PyAbstractClass,PyTypeChecker
    et: ElementTree = ElementTreeFactory(el)
    et.write(
        fp,
        encoding='utf-8',
        method='xml',
        pretty_print=True,
        xml_declaration=False,
        with_tail=False,
        doctype=doctype,
    )
