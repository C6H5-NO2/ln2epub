import json
import os.path
from dataclasses import dataclass

from .workspace_stage import WorkspaceStage
from ..libxml.html import HtmlElement
from ..libxml.xhtml import XHTML_NAMESPACE, xhtml_document, xhtml_dump, xhtml_parse
from ..segmenter.segmenter import Segmenter, is_valid_identifier
from ..util.path import is_valid_filename


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class SegmentStage:
    lang: str
    segmenter: Segmenter
    force: bool = True

    def run(
        self,
        *,
        normalised_xhtml_path: str,
        segments_dir: str,
    ) -> dict[str, str]:
        seg_files: dict[str, str] = dict()
        if not self.force and os.path.isdir(segments_dir):
            listed_files = os.listdir(segments_dir)
            for listed_file in listed_files:
                if listed_file.endswith('.xhtml') and is_valid_filename(listed_file):
                    seg_id = listed_file.removesuffix('.xhtml')
                    if is_valid_identifier(seg_id):
                        seg_path = os.path.join(segments_dir, listed_file)
                        seg_files[seg_id] = seg_path
            print(f'reuse segments in `{segments_dir}`')
            print(json.dumps(seg_files, ensure_ascii=False, indent=2))
            return seg_files

        WorkspaceStage(force=self.force).run(workspace_dir=segments_dir)
        if not os.path.isdir(segments_dir):
            raise NotADirectoryError(segments_dir)

        normed_el = xhtml_parse(normalised_xhtml_path)
        normed_el = normed_el.body[0]
        if normed_el.tag != f'{{{XHTML_NAMESPACE}}}div':
            raise ValueError(normed_el.tag)
        seg_dict = self.segmenter.segment(normed_el)
        for seg_id, seg_el in seg_dict.items():
            seg_file = f'{seg_id}.xhtml'
            if not is_valid_filename(seg_file):
                raise PermissionError(seg_file)
            seg_path = os.path.join(segments_dir, seg_file)
            # *seg_el to drop <section> tag
            seg_el = xhtml_document(*seg_el, lang=self.lang, title=_get_segment_title(seg_id))
            _xhtml_dump_preprocess(seg_el)
            xhtml_dump(seg_el, seg_path)
            seg_files[seg_id] = seg_path

        print(f'segmented to `{segments_dir}`')
        print(json.dumps(seg_dict, ensure_ascii=False, indent=2))
        return seg_files


def _xhtml_dump_preprocess(xhtml: HtmlElement) -> None:
    # todo: better logic?
    for child in xhtml.body.iterchildren():
        if not child.text:
            child.text = ''


def _get_segment_title(segment_id: str) -> str:
    # todo: i18n
    raise NotImplementedError(segment_id)
