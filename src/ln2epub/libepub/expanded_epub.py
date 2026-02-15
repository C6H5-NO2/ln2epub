import os.path
from dataclasses import dataclass
from typing import Final, LiteralString

from .container import ContainerBuilder
from .container_resource import ContainerResourceBuilder
from .navigation_document import NavigationDocumentBuilder
from .package_document import PackageDocumentBuilder
from ..libxml.xhtml import xhtml_document, xhtml_dump
from ..libxml.xml import xml_dump
from ..util.frozenlist import frozenlist
from ..util.path import make_ancestors, require_contained

EPUB: Final[LiteralString] = 'EPUB'
AUDIO: Final[LiteralString] = 'audio'
FONT: Final[LiteralString] = 'font'
IMAGE: Final[LiteralString] = 'image'
SCRIPT: Final[LiteralString] = 'script'
STYLE: Final[LiteralString] = 'style'
TEXT: Final[LiteralString] = 'text'
PACKAGE_OPF: Final[LiteralString] = 'package.opf'
NAV_XHTML: Final[LiteralString] = 'nav.xhtml'


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ExpandedEpubBuilder:
    container_builder: ContainerBuilder
    pacakge_document_builder: PackageDocumentBuilder

    navigation_document_url: str = f'{EPUB}/{NAV_XHTML}'
    navigation_document_builder: NavigationDocumentBuilder

    container_resources: frozenlist[ContainerResourceBuilder]

    def build(self) -> str:
        """
        :return: abs root dir
        """
        root = self.container_builder.build()
        if not os.path.isdir(root):
            raise NotADirectoryError(root)

        package_document = \
            os.path.join(root, self.container_builder.container_file_builder.package_document_url)
        require_contained(package_document, root=root)
        make_ancestors(package_document)
        el = self.pacakge_document_builder.build()
        xml_dump(el, package_document)

        navigation_document = os.path.join(root, self.navigation_document_url)
        require_contained(navigation_document, root=root)
        make_ancestors(navigation_document)
        el = self.navigation_document_builder.build()
        el = xhtml_document(el, lang=self.pacakge_document_builder.dc_language, title='nav')
        xhtml_dump(el, navigation_document)

        for container_resource in self.container_resources:
            container_resource.build(root_directory=root)

        return root
