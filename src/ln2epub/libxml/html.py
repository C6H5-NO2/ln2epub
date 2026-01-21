import lxml.html
import lxml.html.builder

from .xml import ElementMaker

HtmlElement = lxml.html.HtmlElement


def html_element_maker() -> ElementMaker:
    # em = lxml.html.builder.E
    em = ElementMaker(
        makeelement=lxml.html.html_parser.makeelement,
    )
    return em
