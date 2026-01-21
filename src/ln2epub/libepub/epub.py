import os.path

from .container import ContainerBuilder
from .container_file import ContainerFileBuilder
from .package_document import PackageDocumentBuilder
from ..libxml.xml import xml_dump


# todo
def _build_epub(
    container_builder: ContainerBuilder,
    container_file_builder: ContainerFileBuilder,
    pacakge_document_builder: PackageDocumentBuilder,
):
    root_dir = container_builder.build()
    epub_dir = _build_epub_directory(root_dir)

    container_file = os.path.join(root_dir, 'META-INF', 'container.xml')
    container_file_el = container_file_builder.build()
    xml_dump(container_file_el, container_file)

    package_document = os.path.join(root_dir, container_file_builder.package_document)
    package_document_el = pacakge_document_builder.build()
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
