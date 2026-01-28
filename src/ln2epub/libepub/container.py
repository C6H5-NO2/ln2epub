import os.path
from dataclasses import dataclass

from .container_file import ContainerFileBuilder
from ..libxml.xml import xml_dump


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerBuilder:
    root_directory: str
    container_file_builder: ContainerFileBuilder

    def build(self) -> str:
        root = os.path.abspath(self.root_directory)
        if os.path.exists(root):
            raise FileExistsError(root)
        os.makedirs(root)
        # consider shutil.rmtree on error
        self._build(root=root)
        return root

    def _build(self, root: str) -> None:
        mimetype = os.path.join(root, 'mimetype')
        with open(mimetype, 'wt', encoding='ascii', newline='\n') as fp:
            fp.write('application/epub+zip')

        metainf = os.path.join(root, 'META-INF')
        os.makedirs(metainf)

        container_file = os.path.join(metainf, 'container.xml')
        el = self.container_file_builder.build()
        xml_dump(el, container_file)
