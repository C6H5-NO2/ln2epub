import os.path
from dataclasses import dataclass
from typing import Final, LiteralString

from .normalise_stage import NormaliseStage
from .prebuild_stage import PrebuildStage
from .relink_stage import RelinkStage
from .segment_stage import SegmentStage
from .workspace_stage import WorkspaceStage

_NORMALISED_XHTML: Final[LiteralString] = 'normalised.xhtml'
_SEGMENTS_DIR: Final[LiteralString] = 'segments'


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class Pipeline:
    html_path: str
    workspace_dir: str
    workspace_stage: WorkspaceStage
    normalise_stage: NormaliseStage
    segment_stage: SegmentStage
    relink_stage: RelinkStage
    prebuild_stage: PrebuildStage

    def run(self) -> str:
        workspace_dir = self.workspace_stage.run(
            workspace_dir=self.workspace_dir,
        )

        normalised_xhtml_path = os.path.join(workspace_dir, _NORMALISED_XHTML)
        self.normalise_stage.run(
            html_path=self.html_path,
            normalised_xhtml_path=normalised_xhtml_path,
        )

        segments_dir = os.path.join(workspace_dir, _SEGMENTS_DIR)
        segment_result = self.segment_stage.run(
            normalised_xhtml_path=normalised_xhtml_path,
            segments_directory=segments_dir,
        )

        relink_result = self.relink_stage.run(
            segment_paths=list(segment_result.values()),
        )

        expanded_epub_builder = self.prebuild_stage.run(
            segment_result=segment_result,
            relink_result=relink_result,
        )

        return ''
