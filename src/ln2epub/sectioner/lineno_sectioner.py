from .sectioner import is_valid_identifier
from ..libxml.html import HtmlElement
from ..libxml.xhtml import xhtml_element_maker


class LinenoSectioner:
    def __init__(self, sect_ranges: dict[str, range]):
        self._sect_ranges = self._validate_sect_ranges(sect_ranges)
        self._em = xhtml_element_maker()

    def section(self, div: HtmlElement) -> dict[str, HtmlElement]:
        el_iter = div.iterchildren()
        el: HtmlElement | None = next(el_iter, None)
        sect_dict = dict()
        for sect_id, sect_range in self._sect_ranges:
            while el is not None and el.sourceline < sect_range.start:
                el = next(el_iter, None)
            sect_children: list[HtmlElement] = []
            while el is not None and el.sourceline < sect_range.stop:
                sect_children.append(el)
                el = next(el_iter, None)
            if len(sect_children):
                sect_dict[sect_id] = sect_children
            if el is None:
                break

        for sect_id in sect_dict:
            section = self._em.section()
            section.extend(sect_dict[sect_id])
            sect_dict[sect_id] = section

        return sect_dict

    def _validate_sect_ranges(self, ranges: dict[str, range]) -> list[tuple[str, range]]:
        ranges = list(ranges.items())
        ranges.sort(key=lambda it: it[1].start)
        prev = ('(-inf, 1)', range(0, 1))
        for sect_id, sect_range in ranges:
            if not is_valid_identifier(sect_id):
                raise ValueError(f'invalid section identifier `{sect_id}`')
            if not (sect_range.start < sect_range.stop and sect_range.step == 1):
                raise ValueError(f'invalid section range in `{sect_id}`')
            if sect_range.start < prev[1].stop:
                raise ValueError(f'overlapping sections `{sect_id}` and `{prev[0]}`')
            prev = (sect_id, sect_range)
        return ranges
