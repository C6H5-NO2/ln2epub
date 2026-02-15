import os.path
from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerBuilder:
    root_directory: str

    def build(self) -> str:
        """
        :return: abs root dir
        """
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
