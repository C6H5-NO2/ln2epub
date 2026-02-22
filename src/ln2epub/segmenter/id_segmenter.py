from typing import Final, LiteralString

from .segmenter import is_valid_segment_id
from ..libxml.html import HtmlElement
from ..libxml.xhtml import XHTML_NAMESPACE
from ..libxml.xml import QName
from ..version import NAME

_SEGMENT_ID_PREFIX: Final[LiteralString] = NAME + '-'


class IdSegmenter:
    def segment(self, div: HtmlElement) -> dict[str, HtmlElement]:
        """
        :param div: A normalised <div> containing <section id="ln2epub-id">s.
        """
        seg_dict: dict[str, HtmlElement] = dict()
        seg_set: set[HtmlElement] = set()
        for el in div.iterdescendants(QName(XHTML_NAMESPACE, 'section'), 'section'):
            el_id = el.get('id')
            if not el_id or not el_id.startswith(_SEGMENT_ID_PREFIX):
                continue
            seg_id = el_id.removeprefix(_SEGMENT_ID_PREFIX)
            if not is_valid_segment_id(seg_id):
                raise ValueError(f'invalid segment identifier `{seg_id}`')
            if seg_dict.get(seg_id) is not None:
                raise ValueError(f'duplicate segment `{seg_id}`')
            seg_dict[seg_id] = el
            seg_set.add(el)

        for seg_id, el in seg_dict.items():
            for an in el.iterancestors(QName(XHTML_NAMESPACE, 'section'), 'section'):
                if an in seg_set:
                    raise ValueError(f'nested section `{seg_id}`')

        return seg_dict
