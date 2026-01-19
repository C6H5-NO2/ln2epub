from typing import Final

from ..libxml.xhtml import XHTML_NAMESPACE
from ..libxml.xml import ElementMaker, XML_NAMESPACE

EPUB_NAMESPACE: Final[str] = 'http://www.idpf.org/2007/ops'


def epub_xhtml_element_maker() -> ElementMaker:
    return ElementMaker(
        namespace=XHTML_NAMESPACE,
        nsmap={
            None: XHTML_NAMESPACE,
            'xml': XML_NAMESPACE,
            'epub': EPUB_NAMESPACE,
        },
    )
