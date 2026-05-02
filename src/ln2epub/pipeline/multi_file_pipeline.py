from dataclasses import dataclass
from typing import Literal

from .normalise_stage import NormaliseStage
from .prebuild_stage import PrebuildStage
from .relink_stage import RelinkStage
from .segment_stage import SegmentStage
from .workspace_stage import WorkspaceStage
from ..libepub.epubcheck import EpubCheck
from ..util.frozenlist import frozenlist


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class Pipeline:
    workspace_stage: WorkspaceStage
    normalise_stage: NormaliseStage
    segment_stage: SegmentStage
    relink_stage: RelinkStage
    prebuild_stage: PrebuildStage
    epub_check: EpubCheck

    # todo
    def run(
        self,
        *,
        html_paths: frozenlist[str],
        workspace_directory: str,
        run_to: Literal['workspace', 'normalise', 'segment', 'relink', 'prebuild', 'epub'] = 'epub'
    ) -> str:
        raise NotImplementedError()
