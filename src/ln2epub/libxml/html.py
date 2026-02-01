import os.path
from functools import cache

from lxml.builder import ElementMaker as _ElementMaker
from lxml.etree import _ElementTree
from lxml.html import HTMLParser, HtmlElement as _HtmlElement, html_parser, parse

from .xml import ElementMaker

type HtmlElement = _HtmlElement


def html_element_maker() -> ElementMaker[HtmlElement]:
    # em = lxml.html.builder.E
    em = _ElementMaker(
        makeelement=html_parser.makeelement,
    )
    return em


@cache
def _parser():
    return HTMLParser(
        encoding='utf-8',
        remove_blank_text=False,
        remove_comments=True,
        remove_pis=True,
        no_network=True,
        huge_tree=False,
    )


def html_parse(path: str) -> HtmlElement:
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with open(path, 'rb') as fp:
        et: _ElementTree = parse(fp, parser=_parser())
        # note that lxml will keep white spaces (incl \r\n)
        # from lxml.etree import tostring
        # print(tostring(et, encoding='unicode'))
    el: HtmlElement = et.getroot()
    return el
