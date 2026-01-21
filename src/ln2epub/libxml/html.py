from lxml.html import HtmlElement, html_parser

from .xml import ElementMaker

HtmlElement = HtmlElement


def html_element_maker() -> ElementMaker:
    # em = lxml.html.builder.E
    em = ElementMaker(
        makeelement=html_parser.makeelement,
    )
    return em
