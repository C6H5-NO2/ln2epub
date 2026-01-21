import os.path
from dataclasses import dataclass
from functools import cache
from mimetypes import guess_file_type
from typing import Final, Literal, LiteralString
from uuid import uuid4

from ..libxml.xml import Element, ElementMaker, QName, xml_element_maker
from ..util.dataclass import _attr_setter
from ..util.datetime import datetime_iso8601
from ..version import NAME, VERSION

DC_NAMESPACE: Final[LiteralString] = 'http://purl.org/dc/elements/1.1/'
DCTERMS_NAMESPACE: Final[LiteralString] = 'http://purl.org/dc/terms/'
OPF_NAMESPACE: Final[LiteralString] = 'http://www.idpf.org/2007/opf'

_DC_IDENTIFIER_ID: Final[LiteralString] = 'dc-identifier'


def opf_element_maker() -> ElementMaker:
    em = xml_element_maker(
        namespace=OPF_NAMESPACE,
        nsmap={
            None: OPF_NAMESPACE,
            'dc': DC_NAMESPACE,
            'dcterms': DCTERMS_NAMESPACE,
        },
    )
    return em


@cache
def _element_maker() -> ElementMaker:
    return opf_element_maker()


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class PublicationResourceBuilder:
    href: str
    id: str = None
    media_type: str = None
    properties: Literal['cover-image', 'nav', 'scripted'] | str | None = None
    reading_order: int | None = None

    # noinspection PyDataclass
    def __post_init__(self):
        setter = _attr_setter(self)
        if not self.id:
            setter.id = os.path.basename(self.href)
        if not self.media_type:
            setter.media_type, _ = guess_file_type(self.id)

    def _build_manifest_item(self) -> Element:
        em = _element_maker()
        attribs = {
            'href': self.href,
            'id': self.id,
            'media-type': self.media_type,
        }
        if self.properties:
            attribs['properties'] = self.properties
        item = em.item(**attribs)
        return item

    def _build_spine_itemref(self) -> Element:
        em = _element_maker()
        itemref = em.itemref(idref=self.id)
        return itemref


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class PackageDocumentBuilder:
    dc_identifier: str = None
    dc_title: str
    dc_language: str
    dcterms_modified: str = None
    dc_creator: str | None = None
    app_generator: str | None = f'{NAME} v{VERSION}'
    app_generated_by: str | None = None
    items: list[PublicationResourceBuilder]

    # noinspection PyDataclass
    def __post_init__(self):
        setter = _attr_setter(self)
        if not self.dc_identifier:
            setter.dc_identifier = f'urn:uuid:{uuid4()}'
        if not self.dcterms_modified:
            setter.dcterms_modified = datetime_iso8601()

    def build(self) -> Element:
        em = _element_maker()
        metadata = self._build_metadata()
        manifest = self._build_manifest()
        spine = self._build_spine()
        package = em.package(
            metadata,
            manifest,
            spine,
            **{
                'unique-identifier': _DC_IDENTIFIER_ID,
                'version': '3.0',
            },
        )
        return package

    def _build_metadata(self) -> Element:
        em = _element_maker()
        metadata: Element = em.metadata()

        dc_identifier = em(QName(DC_NAMESPACE, 'identifier'), self.dc_identifier, id=_DC_IDENTIFIER_ID)
        dc_title = em(QName(DC_NAMESPACE, 'title'), self.dc_title)
        dc_language = em(QName(DC_NAMESPACE, 'language'), self.dc_language)
        metadata.extend([dc_identifier, dc_title, dc_language])

        if self.dc_creator:
            dc_creator = em(QName(DC_NAMESPACE, 'creator'), self.dc_creator)
            metadata.append(dc_creator)

        dcterms_modified = em.meta(self.dcterms_modified, property='dcterms:modified')
        metadata.append(dcterms_modified)

        if self.app_generator:
            app_generator = em.meta(self.app_generator, property='app:generator')
            metadata.append(app_generator)

        if self.app_generated_by:
            app_generated_by = em.meta(self.app_generated_by, property='app:generated-by')
            metadata.append(app_generated_by)

        return metadata

    def _build_manifest(self) -> Element:
        em = _element_maker()
        manifest: Element = em.manifest()
        for it in self.items:
            item = it._build_manifest_item()
            manifest.append(item)
        return manifest

    def _build_spine(self) -> Element:
        em = _element_maker()
        spine: Element = em.spine()
        items = sorted(
            (it for it in self.items if it.reading_order is not None),
            key=lambda it: it.reading_order,
        )
        for it in items:
            itemref = it._build_spine_itemref()
            spine.append(itemref)
        return spine
