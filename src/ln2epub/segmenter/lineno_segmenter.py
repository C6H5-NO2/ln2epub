from .segmenter import is_valid_segment_id
from ..libxml.html import HtmlElement
from ..libxml.xhtml import xhtml_element_maker
from ..libxml.xml import ElementMaker
from ..util.frozendict import frozendict
from ..util.frozenlist import frozenlist


class LinenoSegmenter:
    def __init__(self, seg_ranges: frozendict[str, range]):
        self._seg_ranges: frozenlist[tuple[str, range]] = self._validate_seg_ranges(seg_ranges)
        self._em: ElementMaker[HtmlElement] = xhtml_element_maker()

    def segment(self, div: HtmlElement) -> dict[str, HtmlElement]:
        """
        :param div: A normalised <div> with source line number metadata.
        """
        if div.sourceline is None:
            raise ValueError('source line unknown')
        el_iter = div.iterchildren()
        el: HtmlElement | None = next(el_iter, None)
        seg_dict = dict()
        for seg_id, seg_range in self._seg_ranges:
            while el is not None and el.sourceline < seg_range.start:
                el = next(el_iter, None)
            seg_children: list[HtmlElement] = []
            while el is not None and el.sourceline < seg_range.stop:
                seg_children.append(el)
                el = next(el_iter, None)
            if len(seg_children):
                seg_dict[seg_id] = seg_children
            if el is None:
                break

        for seg_id in seg_dict:
            section = self._em.section()
            section.extend(seg_dict[seg_id])
            seg_dict[seg_id] = section

        return seg_dict

    def _validate_seg_ranges(self, ranges: frozendict[str, range]) -> list[tuple[str, range]]:
        ranges = list(ranges.items())
        ranges.sort(key=lambda it: it[1].start)
        prev = ('(-inf, 1)', range(0, 1))
        for seg_id, seg_range in ranges:
            if not is_valid_segment_id(seg_id):
                raise ValueError(f'invalid segment identifier `{seg_id}`')
            if not (seg_range.start < seg_range.stop and seg_range.step == 1):
                raise ValueError(f'invalid segment range in `{seg_id}`')
            if seg_range.start < prev[1].stop:
                raise ValueError(f'overlapping segments `{seg_id}` and `{prev[0]}`')
            prev = (seg_id, seg_range)
        return ranges
