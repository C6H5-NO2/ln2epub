from dataclasses import dataclass
from typing import Final

from ..libxml.xml import Element, ElementMaker

_CONTAINER_NAMESPACE: Final[str] = 'urn:oasis:names:tc:opendocument:xmlns:container'


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerFileBuilder:
    package_document: str = 'EPUB/package.opf'


def build_container_file(arg: ContainerFileBuilder) -> Element:
    em = ElementMaker(
        namespace=_CONTAINER_NAMESPACE,
        nsmap={
            None: _CONTAINER_NAMESPACE,
        },
    )
    container = em.container(
        em.rootfiles(
            em.rootfile(
                **{
                    'full-path': arg.package_document,
                    'media-type': 'application/oebps-package+xml'
                },
            )
        ),
        version='1.0',
    )
    return container
