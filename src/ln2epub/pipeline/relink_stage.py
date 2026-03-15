import json
from dataclasses import dataclass

from ..libxml.xhtml import xhtml_dump, xhtml_parse
from ..relinker.relinker import Relinker
from ..util.frozenlist import frozenlist


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class RelinkStage:
    relinker: Relinker

    def run(
        self,
        *,
        segment_paths: frozenlist[str],
    ) -> dict[str, str]:
        relinked: dict[str, str] = dict()
        for seg_path in segment_paths:
            seg_xhtml_el = xhtml_parse(seg_path)
            rst = self.relinker.relink(seg_xhtml_el.body)
            relinked |= rst
            xhtml_dump(seg_xhtml_el, seg_path, compact=True)
        print('relinked')
        print(json.dumps(relinked, ensure_ascii=False, indent=2, sort_keys=True))
        return relinked
