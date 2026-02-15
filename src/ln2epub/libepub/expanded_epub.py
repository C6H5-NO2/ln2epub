import os.path
from dataclasses import dataclass, replace as dataclass_replace

from .consts import EPUB, NAV_XHTML, PACKAGE_OPF, TOC_NCX
from .container import ContainerBuilder
from .container_file import ContainerFileBuilder
from .container_resource import ContainerResourceBuilder
from .navigation_document import NavigationDocumentBuilder
from .ncx import NcxBuilder
from .package_document import PackageDocumentBuilder, PublicationResourceItemBuilder
from ..libxml.xhtml import xhtml_document, xhtml_dump
from ..libxml.xml import xml_dump
from ..util.frozenlist import frozenlist
from ..util.path import make_ancestors, relative_url, require_contained


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ExpandedEpubBuilder:
    container_builder: ContainerBuilder
    container_file_builder: ContainerFileBuilder

    package_document_url: str = f'{EPUB}/{PACKAGE_OPF}'
    pacakge_document_builder: PackageDocumentBuilder

    navigation_document_url: str = f'{EPUB}/{NAV_XHTML}'
    navigation_document_builder: NavigationDocumentBuilder
    support_legacy_ncx: bool = False

    container_resources: frozenlist[ContainerResourceBuilder]

    def build(self) -> str:
        """
        :return: abs root dir
        """
        root = self.container_builder.build()
        if not os.path.isdir(root):
            raise NotADirectoryError(root)

        container_file = os.path.join(root, 'META-INF', 'container.xml')
        require_contained(container_file, root=root)
        el = self.container_file_builder.build()
        xml_dump(el, container_file)
        del el

        package_document = os.path.join(root, self.package_document_url)
        require_contained(package_document, root=root)
        make_ancestors(package_document)
        if self.support_legacy_ncx:
            ncx_url = os.path.join(os.path.dirname(self.navigation_document_url), TOC_NCX)
            ncx = os.path.join(root, ncx_url)
            ncx_pri_builder = PublicationResourceItemBuilder(
                href=relative_url(path=ncx, start=package_document, root=root),
                media_type='application/x-dtbncx+xml',
            )
            pacakge_document_builder = dataclass_replace(
                self.pacakge_document_builder,
                items=[*self.pacakge_document_builder.items, ncx_pri_builder],
            )
            el = pacakge_document_builder.build()
            spine = next(el.iterchildren('{*}spine'), None)
            spine.set('toc', ncx_pri_builder.id)
        else:
            el = self.pacakge_document_builder.build()
        xml_dump(el, package_document)
        del el

        navigation_document = os.path.join(root, self.navigation_document_url)
        require_contained(navigation_document, root=root)
        make_ancestors(navigation_document)
        el = self.navigation_document_builder.build()
        el = xhtml_document(el, lang=self.pacakge_document_builder.dc_language, title='nav')
        xhtml_dump(el, navigation_document)
        del el

        if self.support_legacy_ncx:
            ncx_builder = NcxBuilder(
                nav_builder=self.navigation_document_builder,
                dc_identifier=self.pacakge_document_builder.dc_identifier,
            )
            el = ncx_builder.build()
            xml_dump(el, ncx)
            del el

        for container_resource in self.container_resources:
            container_resource.build(root_directory=root)

        return root
