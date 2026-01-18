import os.path

from .container import ContainerBuilder, build_container
from .container_file import ContainerFileBuilder, build_container_file
from .package_document import PackageDocumentBuilder, build_package_document
from ..libxml.xml import dump as xml_dump


def _build_epub(
    container_builder: ContainerBuilder,
    container_file_builder: ContainerFileBuilder,
    pacakge_document_builder: PackageDocumentBuilder,
):
    root_dir = build_container(container_builder)
    epub_dir = _build_epub_directory(root_dir)

    container_file = os.path.join(root_dir, 'META-INF', 'container.xml')
    container_file_el = build_container_file(container_file_builder)
    xml_dump(container_file_el, container_file)

    package_document = os.path.join(root_dir, container_file_builder.package_document)
    package_document_el = build_package_document(pacakge_document_builder)
    xml_dump(package_document_el, package_document)


def _build_epub_directory(root_dir: str) -> str:
    epub_dir = os.path.join(root_dir, 'EPUB')
    os.makedirs(epub_dir)

    media_types = [
        'audio',
        'font',
        'image',
        'script',
        'style',
        'text',
    ]
    for media_type in media_types:
        os.makedirs(os.path.join(epub_dir, media_type))

    return epub_dir
