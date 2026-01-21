import os.path
from dataclasses import dataclass

from .container_file import ContainerFileBuilder
from ..libxml.xml import xml_dump


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerBuilder:
    root_directory: str
    container_file_builder: ContainerFileBuilder

    def build(self) -> str:
        root_dir = os.path.abspath(self.root_directory)
        if os.path.exists(root_dir):
            raise FileExistsError(root_dir)
        os.makedirs(root_dir)

        mimetype = os.path.join(root_dir, 'mimetype')
        with open(mimetype, 'wt', encoding='ascii', newline='\n') as fp:
            fp.write('application/epub+zip')

        metainf = os.path.join(root_dir, 'META-INF')
        os.makedirs(metainf)

        container_file = os.path.join(metainf, 'container.xml')
        container_file_el = self.container_file_builder.build()
        xml_dump(container_file_el, container_file)

        return root_dir
