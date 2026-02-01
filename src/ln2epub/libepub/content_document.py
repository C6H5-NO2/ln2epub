from typing import Final, LiteralString

from ..libxml.html import HtmlElement
from ..libxml.xhtml import xhtml_element_maker
from ..libxml.xml import ElementMaker

EPUB_NAMESPACE: Final[LiteralString] = 'http://www.idpf.org/2007/ops'


def epub_xhtml_element_maker() -> ElementMaker[HtmlElement]:
    em = xhtml_element_maker(nsmap={
        'epub': EPUB_NAMESPACE,
    })
    return em
