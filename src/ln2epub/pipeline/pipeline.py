import os.path
from dataclasses import dataclass
from functools import partial
from typing import Final, Literal, LiteralString

from .normalise_stage import NormaliseStage
from .prebuild_stage import PrebuildStage
from .relink_stage import RelinkStage
from .segment_stage import SegmentStage
from .workspace_stage import WorkspaceStage
from ..libepub.epubcheck import EpubCheck
from ..normaliser.normaliser import Normaliser
from ..normaliser.selector import Selector
from ..relinker.relinker import Relinker
from ..segmenter.segment_order_provider import SegmentOrderProvider
from ..segmenter.segment_title_provider import SegmentTitleProvider
from ..segmenter.segmenter import Segmenter
from ..util.dataclass import _attr_setter

_NORMALISED_XHTML: Final[LiteralString] = 'normalised.xhtml'
_SEGMENTS_DIR: Final[LiteralString] = 'segments'
_EXPANDED_EPUB_DIR: Final[LiteralString] = 'release'


# noinspection PyDataclass,PyTypeChecker
def build_normalise_pipeline(
    *,
    lang: str,
    selector: Selector,
    normaliser: Normaliser,
) -> Pipeline:
    pipeline = Pipeline(
        workspace_stage=WorkspaceStage(),
        normalise_stage=NormaliseStage(
            selector=selector,
            normaliser=normaliser,
            lang=lang,
        ),
        segment_stage=None,
        relink_stage=None,
        prebuild_stage=None,
        epub_check=None,
    )
    setter = _attr_setter(pipeline)
    setter.run = partial(Pipeline.run, pipeline, run_until='normalise')
    return pipeline


def build_pipeline(
    *,
    lang: str,
    selector: Selector,
    normaliser: Normaliser,
    segmenter: Segmenter,
    segment_order_provider: SegmentOrderProvider,
    segment_title_provider: SegmentTitleProvider,
    relinker: Relinker,
    dc_title: str,
    dc_creator: str,
    app_generated_by: str,
    cover_id: str,
    epub_check: EpubCheck,
) -> Pipeline:
    return Pipeline(
        workspace_stage=WorkspaceStage(),
        normalise_stage=NormaliseStage(
            selector=selector,
            normaliser=normaliser,
            lang=lang,
        ),
        segment_stage=SegmentStage(
            segmenter=segmenter,
            segment_title_provider=segment_title_provider,
            lang=lang,
        ),
        relink_stage=RelinkStage(
            relinker=relinker,
        ),
        prebuild_stage=PrebuildStage(
            lang=lang,
            dc_title=dc_title,
            dc_creator=dc_creator,
            app_generated_by=app_generated_by,
            cover_id=cover_id,
            segment_order_provider=segment_order_provider,
            segment_title_provider=segment_title_provider,
        ),
        epub_check=epub_check,
    )


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class Pipeline:
    workspace_stage: WorkspaceStage
    normalise_stage: NormaliseStage
    segment_stage: SegmentStage
    relink_stage: RelinkStage
    prebuild_stage: PrebuildStage
    epub_check: EpubCheck

    def run(
        self,
        *,
        html_path: str,
        workspace_directory: str,
        run_to: Literal['workspace', 'normalise', 'segment', 'relink', 'prebuild', 'epub'] = 'epub'
    ) -> str:
        workspace_directory = self.workspace_stage.run(
            workspace_directory=workspace_directory,
        )
        if run_to == 'workspace':
            return workspace_directory

        normalised_xhtml_path = os.path.join(workspace_directory, _NORMALISED_XHTML)
        normalised_xhtml_path = self.normalise_stage.run(
            html_path=html_path,
            normalised_xhtml_path=normalised_xhtml_path,
        )
        if run_to == 'normalise':
            return normalised_xhtml_path

        segments_directory = os.path.join(workspace_directory, _SEGMENTS_DIR)
        segment_result = self.segment_stage.run(
            normalised_xhtml_path=normalised_xhtml_path,
            segments_directory=segments_directory,
        )
        if run_to == 'segment':
            return segments_directory

        relink_result = self.relink_stage.run(
            segment_paths=list(segment_result.values()),
        )
        if run_to == 'relink':
            return segments_directory

        root_directory = os.path.join(workspace_directory, _EXPANDED_EPUB_DIR)
        expanded_epub_builder = self.prebuild_stage.run(
            root_directory=root_directory,
            segment_result=segment_result,
            relink_result=relink_result,
        )
        root_directory = expanded_epub_builder.build()
        print(f'expanded epub in `{root_directory}`')
        if run_to == 'prebuild':
            return root_directory

        epub_path = self.epub_check.run(root_directory=root_directory)
        print(f'saved to `{epub_path}`')
        return epub_path
