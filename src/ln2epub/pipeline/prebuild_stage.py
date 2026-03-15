import os.path
from dataclasses import dataclass, replace as dataclass_replace

from ..libepub.consts import EPUB, NAV_XHTML, PACKAGE_OPF, TEXT
from ..libepub.container import ContainerBuilder
from ..libepub.container_file import ContainerFileBuilder
from ..libepub.container_resource import ContainerResourceBuilder
from ..libepub.expanded_epub import ExpandedEpubBuilder
from ..libepub.navigation_document import NavigationDocumentBuilder, NavigationItemBuilder
from ..libepub.package_document import PackageDocumentBuilder, PublicationResourceItemBuilder
from ..segmenter.segment_order_provider import SegmentOrderProvider
from ..segmenter.segment_title_provider import SegmentTitleProvider
from ..util.frozendict import frozendict
from ..util.path import relative_url


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class PrebuildStage:
    root_directory: str

    lang: str
    dc_title: str
    dc_creator: str | None = None
    app_generated_by: str | None = None

    cover_id: str | None = None
    segment_order_provider: SegmentOrderProvider
    segment_title_provider: SegmentTitleProvider

    text_url: str = f'{EPUB}/{TEXT}'
    package_document_url: str = f'{EPUB}/{PACKAGE_OPF}'
    navigation_document_url: str = f'{EPUB}/{NAV_XHTML}'

    def run(
        self,
        *,
        segment_result: frozendict[str, str],
        relink_result: frozendict[str, str],
    ) -> ExpandedEpubBuilder:
        package_document_builder = self._get_package_document_builder(
            segment_result=segment_result,
            relink_result=relink_result,
        )
        navigation_document_builder = self._get_navigation_document_builder(
            segment_result=segment_result,
        )
        container_resource_builders = self._get_container_resource_builders(
            segment_result=segment_result,
            relink_result=relink_result,
        )
        expanded_epub_builder = self._get_expanded_epub_builder(
            package_document_builder=package_document_builder,
            navigation_document_builder=navigation_document_builder,
            container_resource_builders=container_resource_builders,
        )
        return expanded_epub_builder

    def _get_package_document_builder(
        self,
        *,
        segment_result: frozendict[str, str],
        relink_result: frozendict[str, str],
    ) -> PackageDocumentBuilder:
        pribs: list[PublicationResourceItemBuilder] = []

        for seg_id, seg_path in segment_result.items():
            dst_url = self._get_seg_url(seg_path)
            href = self._get_href(dst_url, start=self.package_document_url)
            prib = PublicationResourceItemBuilder(
                href=href,
                reading_order=self.segment_order_provider.get_order(seg_id)
            )
            pribs.append(prib)

        for dst_url, src_path in relink_result.items():
            href = self._get_href(dst_url, start=self.package_document_url)
            prib = PublicationResourceItemBuilder(
                href=href,
            )
            if self.cover_id and prib.id == self.cover_id:
                prib = dataclass_replace(prib, properties='cover-image')
            pribs.append(prib)
        if self.cover_id and not any(prib for prib in pribs if prib.properties == 'cover-image'):
            raise ValueError(self.cover_id)

        dst_url = self.navigation_document_url
        href = self._get_href(dst_url, start=self.package_document_url)
        prib = PublicationResourceItemBuilder(
            href=href,
            id='nav',
            properties='nav',
        )
        pribs.append(prib)

        pdb = PackageDocumentBuilder(
            dc_title=self.dc_title,
            dc_language=self.lang,
            dc_creator=self.dc_creator,
            app_generated_by=self.app_generated_by,
            items=pribs,
        )
        return pdb

    def _get_navigation_document_builder(
        self,
        *,
        segment_result: frozendict[str, str],
    ) -> NavigationDocumentBuilder:
        nibs: list[NavigationItemBuilder] = []
        seg_ids = list(segment_result.keys())
        seg_ids.sort(key=lambda seg_id: self.segment_order_provider.get_order(seg_id))
        for seg_id in seg_ids:
            title = self.segment_title_provider.get_title(seg_id)
            seg_url = self._get_seg_url(segment_result[seg_id])
            href = self._get_href(seg_url, start=self.navigation_document_url)
            nib = NavigationItemBuilder(
                text=title,
                href=href,
            )
            nibs.append(nib)

        ndb = NavigationDocumentBuilder(
            heading=self.dc_title,
            items=nibs,
        )
        return ndb

    def _get_container_resource_builders(
        self,
        *,
        segment_result: frozendict[str, str],
        relink_result: frozendict[str, str],
    ) -> list[ContainerResourceBuilder]:
        crbs: list[ContainerResourceBuilder] = []

        for seg_id, seg_path in segment_result.items():
            dst_url = self._get_seg_url(seg_path)
            crb = ContainerResourceBuilder(src_path=seg_path, dst_url=dst_url)
            crbs.append(crb)

        for dst_url, src_path in relink_result.items():
            crb = ContainerResourceBuilder(src_path=src_path, dst_url=dst_url)
            crbs.append(crb)

        return crbs

    def _get_expanded_epub_builder(
        self,
        *,
        package_document_builder: PackageDocumentBuilder,
        navigation_document_builder: NavigationDocumentBuilder,
        container_resource_builders: list[ContainerResourceBuilder],
    ) -> ExpandedEpubBuilder:
        eeb = ExpandedEpubBuilder(
            container_builder=ContainerBuilder(
                root_directory=self.root_directory
            ),
            container_file_builder=ContainerFileBuilder(
                package_document_url=self.package_document_url,
            ),
            package_document_url=self.package_document_url,
            pacakge_document_builder=package_document_builder,
            navigation_document_url=self.navigation_document_url,
            navigation_document_builder=navigation_document_builder,
            support_legacy_ncx=True,
            container_resource_builders=container_resource_builders,
        )
        return eeb

    def _get_seg_url(self, seg_path: str) -> str:
        return f'{self.text_url}/{os.path.basename(seg_path)}'

    def _get_href(self, path: str, *, start: str) -> str:
        href = relative_url(
            path=path,
            start=start,
            root=self.root_directory,
            mode='url',
        )
        if not href:
            raise PermissionError(path)
        return href
