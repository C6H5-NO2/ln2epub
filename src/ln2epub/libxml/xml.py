import lxml.builder
import lxml.etree

XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'

# noinspection PyProtectedMember
Element = lxml.etree._Element
ElementMaker = lxml.builder.ElementMaker
QName = lxml.etree.QName


def dump(el: Element, fp) -> None:
    if not hasattr(fp, 'write'):
        with open(fp, 'wb') as fp:
            dump(el, fp)
        return
    # noinspection PyAbstractClass,PyProtectedMember,PyTypeChecker
    et: lxml.etree._ElementTree = lxml.etree.ElementTree(el)
    et.write(
        fp,
        encoding='utf-8',
        method='xml',
        pretty_print=True,
        xml_declaration=False,
        with_tail=False,
        doctype='<?xml version="1.0" encoding="utf-8"?>',
    )
