from typing import Final, LiteralString

from .sectioner import is_valid_identifier
from ..libxml.html import HtmlElement
from ..libxml.xhtml import XHTML_NAMESPACE
from ..libxml.xml import QName
from ..version import NAME

ID_PREFIX: Final[LiteralString] = NAME + '-'


class IdSectioner:
    def section(self, html: HtmlElement) -> dict[str, HtmlElement]:
        sect_dict: dict[str, HtmlElement] = dict()
        sect_set: set[HtmlElement] = set()
        for el in html.iterdescendants(QName(XHTML_NAMESPACE, 'section'), 'section'):
            el_id = el.get('id')
            if not el_id or not el_id.startswith(ID_PREFIX):
                continue
            sect_id = el_id.removeprefix(ID_PREFIX)
            if not is_valid_identifier(sect_id):
                raise ValueError(f'invalid section identifier `{sect_id}`')
            if sect_dict.get(sect_id) is not None:
                raise ValueError(f'duplicate section `{sect_id}`')
            sect_dict[sect_id] = el
            sect_set.add(el)

        for sect_id, el in sect_dict.items():
            for an in el.iterancestors(QName(XHTML_NAMESPACE, 'section'), 'section'):
                if an in sect_set:
                    raise ValueError(f'nested section `{sect_id}`')

        return sect_dict
