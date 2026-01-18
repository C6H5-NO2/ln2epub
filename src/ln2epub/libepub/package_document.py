import os.path
from dataclasses import dataclass
from mimetypes import guess_file_type
from typing import Final, Literal
from uuid import uuid4

from .. import PACKAGE_NAME, PACKAGE_VERSION
from ..libxml.xml import Element, ElementMaker, QName
# noinspection PyProtectedMember
from ..util.dataclass import _attr_setter
from ..util.datetime import datetime_iso8601

_DC_IDENTIFIER_ID: Final[str] = 'dc-identifier'
_DC_NAMESPACE: Final[str] = 'http://purl.org/dc/elements/1.1/'


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


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class PackageDocumentBuilder:
    dc_identifier: str = None
    dc_title: str
    dc_language: str
    dcterms_modified: str = None
    dc_creator: str | None = None
    app_generator: str | None = f'{PACKAGE_NAME} v{PACKAGE_VERSION}'
    app_generated_by: str | None = None
    items: list[PublicationResourceBuilder]

    # noinspection PyDataclass
    def __post_init__(self):
        setter = _attr_setter(self)
        if not self.dc_identifier:
            setter.dc_identifier = f'urn:uuid:{uuid4()}'
        if not self.dcterms_modified:
            setter.dcterms_modified = datetime_iso8601()


def build_package_document(arg: PackageDocumentBuilder) -> Element:
    em = ElementMaker(nsmap={
        None: 'http://www.idpf.org/2007/opf',
        'dc': _DC_NAMESPACE,
        'dcterms': 'http://purl.org/dc/terms/',
    })
    metadata = _build_metadata(arg, em)
    manifest = _build_manifest(arg, em)
    spine = _build_spine(arg, em)
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


def _build_metadata(arg: PackageDocumentBuilder, em: ElementMaker) -> Element:
    metadata: Element = em.metadata()

    dc_identifier = em(QName(_DC_NAMESPACE, 'identifier'), arg.dc_identifier, id=_DC_IDENTIFIER_ID)
    dc_title = em(QName(_DC_NAMESPACE, 'title'), arg.dc_title)
    dc_language = em(QName(_DC_NAMESPACE, 'language'), arg.dc_language)
    metadata.extend([dc_identifier, dc_title, dc_language])

    if arg.dc_creator:
        dc_creator = em(QName(_DC_NAMESPACE, 'creator'), arg.dc_creator)
        metadata.append(dc_creator)

    dcterms_modified = em.meta(arg.dcterms_modified, property='dcterms:modified')
    metadata.append(dcterms_modified)

    if arg.app_generator:
        app_generator = em.meta(arg.app_generator, property='app:generator')
        metadata.append(app_generator)

    if arg.app_generated_by:
        app_generated_by = em.meta(arg.app_generated_by, property='app:generated-by')
        metadata.append(app_generated_by)

    return metadata


def _build_manifest(arg: PackageDocumentBuilder, em: ElementMaker) -> Element:
    manifest: Element = em.manifest()
    for it in arg.items:
        attrs = {
            'href': it.href,
            'id': it.id,
            'media-type': it.media_type,
        }
        if it.properties:
            attrs['properties'] = it.properties
        item = em.item(**attrs)
        manifest.append(item)
    return manifest


def _build_spine(arg: PackageDocumentBuilder, em: ElementMaker) -> Element:
    spine: Element = em.spine()
    items = sorted((it for it in arg.items if it.reading_order is not None), key=lambda it: it.reading_order)
    for it in items:
        itemref = em.itemref(idref=it.id)
        spine.append(itemref)
    return spine
