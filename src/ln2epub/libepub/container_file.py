from dataclasses import dataclass

from ..libxml.xml import Element, ElementMaker


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerFileBuilder:
    package_document: str


def build_container_file(arg: ContainerFileBuilder) -> Element:
    em = ElementMaker(nsmap={
        None: 'urn:oasis:names:tc:opendocument:xmlns:container',
    })
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
