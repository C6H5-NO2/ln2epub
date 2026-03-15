import json
import os.path
from dataclasses import dataclass

from .workspace_stage import WorkspaceStage
from ..libxml.xhtml import XHTML_NAMESPACE, xhtml_document, xhtml_dump, xhtml_parse
from ..segmenter.segment_title_provider import SegmentTitleProvider
from ..segmenter.segmenter import Segmenter, is_valid_segment_id
from ..util.path import is_valid_filename


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class SegmentStage:
    segmenter: Segmenter
    segment_title_provider: SegmentTitleProvider
    lang: str
    force: bool = True

    def run(
        self,
        *,
        normalised_xhtml_path: str,
        segments_directory: str,
    ) -> dict[str, str]:
        seg_files: dict[str, str] = dict()
        if not self.force and os.path.isdir(segments_directory):
            listed_files = os.listdir(segments_directory)
            for listed_file in listed_files:
                if listed_file.endswith('.xhtml') and is_valid_filename(listed_file):
                    seg_id = listed_file.removesuffix('.xhtml')
                    if is_valid_segment_id(seg_id):
                        seg_path = os.path.join(segments_directory, listed_file)
                        seg_files[seg_id] = seg_path
            print(f'reuse segments in `{segments_directory}`')
            print(json.dumps(seg_files, ensure_ascii=False, indent=2, sort_keys=True))
            return seg_files

        WorkspaceStage(force=self.force).run(workspace_directory=segments_directory)
        if not os.path.isdir(segments_directory):
            raise NotADirectoryError(segments_directory)

        normed_el = xhtml_parse(normalised_xhtml_path)
        normed_el = normed_el.body[0]
        if normed_el.tag != f'{{{XHTML_NAMESPACE}}}div':
            raise ValueError(normed_el.tag)
        seg_dict = self.segmenter.segment(normed_el)
        for seg_id, seg_el in seg_dict.items():
            seg_file = f'{seg_id}.xhtml'
            if not is_valid_filename(seg_file):
                raise PermissionError(seg_file)
            seg_path = os.path.join(segments_directory, seg_file)
            seg_el = xhtml_document(
                *seg_el,  # *seg_el to drop <section> tag
                lang=self.lang,
                title=self.segment_title_provider.get_title(seg_id),
            )
            xhtml_dump(seg_el, seg_path, compact=True)
            seg_files[seg_id] = seg_path

        print(f'segmented to `{segments_directory}`')
        print(json.dumps(seg_files, ensure_ascii=False, indent=2, sort_keys=True))
        return seg_files
