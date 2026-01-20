import lxml.html
import lxml.html.builder

from .xml import ElementMaker

HtmlElement = lxml.html.HtmlElement


def html_element_maker() -> ElementMaker:
    return lxml.html.builder.E
