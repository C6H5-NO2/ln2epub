from typing import Final, LiteralString, TYPE_CHECKING

import lxml.builder
import lxml.etree

ElementMaker = lxml.builder.ElementMaker
QName = lxml.etree.QName

# dark magic for (some) type annotations in PyCharm
if not TYPE_CHECKING:
    ElementTree = lxml.etree.ElementTree
    Element = lxml.etree.Element
else:
    ElementTree = lxml.etree._ElementTree
    Element = lxml.etree._Element

XML_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/XML/1998/namespace'
XMLNS_NAMESPACE: Final[LiteralString] = 'http://www.w3.org/2000/xmlns/'


def xml_element_maker() -> ElementMaker:
    return lxml.builder.E


def xml_dump(
    el: Element,
    fp,
    *,
    doctype='<?xml version="1.0" encoding="utf-8"?>',
) -> None:
    if not hasattr(fp, 'write'):
        with open(fp, 'wb') as fp:
            xml_dump(el, fp, doctype=doctype)
        return
    et = ElementTree(el)
    et.write(
        fp,
        encoding='utf-8',
        method='xml',
        pretty_print=True,
        xml_declaration=False,
        with_tail=False,
        doctype=doctype,
    )
