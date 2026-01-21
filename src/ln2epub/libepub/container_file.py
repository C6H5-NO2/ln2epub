from dataclasses import dataclass
from functools import cache
from typing import Final, LiteralString

from ..libxml.xml import Element, ElementMaker, xml_element_maker

CONTAINER_NAMESPACE: Final[LiteralString] = 'urn:oasis:names:tc:opendocument:xmlns:container'


def container_element_maker() -> ElementMaker:
    em = xml_element_maker(
        namespace=CONTAINER_NAMESPACE,
        nsmap={
            None: CONTAINER_NAMESPACE,
        },
    )
    return em


@cache
def _element_maker() -> ElementMaker:
    return container_element_maker()


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerFileBuilder:
    package_document: str

    def build(self) -> Element:
        em = _element_maker()
        container = em.container(
            em.rootfiles(
                em.rootfile(
                    **{
                        'full-path': self.package_document,
                        'media-type': 'application/oebps-package+xml'
                    },
                )
            ),
            version='1.0',
        )
        return container
