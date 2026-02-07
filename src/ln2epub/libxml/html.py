from io import Reader, Writer
from typing import Final

from lxml.builder import ElementMaker as _ElementMaker
from lxml.etree import _ElementTree
from lxml.html import (
    HTMLParser,
    HtmlElement as _HtmlElement,
    html_parser as _lxml_html_parser,
    parse as _lxml_html_parse,
)

from .xml import ElementMaker, _xml_dump

type HtmlElement = _HtmlElement


def html_element_maker() -> ElementMaker[HtmlElement]:
    # em = lxml.html.builder.E
    em = _ElementMaker(
        makeelement=_lxml_html_parser.makeelement,
    )
    return em


def html_parse(fp: str | Reader[bytes], /) -> HtmlElement:
    return _html_parse(fp, parser=_html_parser)


def _html_parse(
    fp: str | Reader[bytes],
    /,
    *,
    parser,
) -> HtmlElement:
    if not hasattr(fp, 'read'):
        with open(fp, 'rb') as fp:
            el = _html_parse(fp, parser=parser)
        return el
    et: _ElementTree = _lxml_html_parse(fp, parser=parser)
    # note that lxml will keep white spaces (incl \r\n)
    # from lxml.etree import tostring
    # print(tostring(et, encoding='unicode'))
    el: HtmlElement = et.getroot()
    return el


def html_dump(el: HtmlElement, fp: str | Writer[bytes], /) -> None:
    _xml_dump(
        el,
        fp,
        method='html',
        doctype='<!DOCTYPE html>',
    )


_html_parser: Final[HTMLParser] = HTMLParser(
    encoding='utf-8',
    remove_blank_text=False,
    remove_comments=True,
    remove_pis=True,
    no_network=True,
    huge_tree=False,
)
