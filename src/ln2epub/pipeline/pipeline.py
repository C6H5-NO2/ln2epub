import os.path
from dataclasses import dataclass
from typing import Final, LiteralString

from .normalise_stage import NormaliseStage
from .segment_stage import SegmentStage
from .workspace_stage import WorkspaceStage

_NORMALISED_XHTML: Final[LiteralString] = 'normalised.xhtml'
_SEGMENTS_DIR: Final[LiteralString] = 'segments'


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class Pipeline:
    workspace_dir: str
    workspace_stage: WorkspaceStage
    normalise_stage: NormaliseStage
    segment_stage: SegmentStage

    def run(self) -> str:
        workspace_dir = self.workspace_stage.run(
            workspace_dir=self.workspace_dir,
        )

        normalised_xhtml_path = os.path.join(workspace_dir, _NORMALISED_XHTML)
        self.normalise_stage.run(
            normalised_xhtml_path=normalised_xhtml_path,
        )

        segments_dir = os.path.join(workspace_dir, _SEGMENTS_DIR)
        self.segment_stage.run(
            normalised_xhtml_path=normalised_xhtml_path,
            segments_dir=segments_dir,
        )

        return workspace_dir
