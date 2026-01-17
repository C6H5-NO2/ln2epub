import uuid
from dataclasses import dataclass, field

from .utils import DATACLASS_KWARGS, FIELD_KWARGS, datetime_iso8601
from ..libxml.xml import Element, ElementMaker, QName

_DC_IDENTIFIER_ID: str = 'dc-identifier'
_DC_NAMESPACE: str = 'http://purl.org/dc/elements/1.1/'


@dataclass(**DATACLASS_KWARGS)
class PackageDocumentBuilder:
    dc_identifier: str = field(default_factory=lambda: f'urn:uuid:{uuid.uuid4()}', **FIELD_KWARGS)
    dc_title: str = ''
    dc_language: str = ''
    dcterms_modified: str = field(default_factory=lambda: datetime_iso8601(), **FIELD_KWARGS)

    dc_creator: str | None = None


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


def _refine():
    field(default_factory=lambda: f'urn:uuid:{uuid.uuid4()}')


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

    return metadata


def _build_manifest(arg: PackageDocumentBuilder, em: ElementMaker) -> Element:
    manifest = em.manifest()
    return manifest


def _build_spine(arg: PackageDocumentBuilder, em: ElementMaker) -> Element:
    spine = em.spine()
    return spine
