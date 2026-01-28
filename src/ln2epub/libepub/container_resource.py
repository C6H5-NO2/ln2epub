import os.path
from dataclasses import dataclass
from shutil import copyfile

from ..util.path import make_ancestors, require_contained


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerResourceBuilder:
    src_path: str
    dst_url: str

    def build(self, root_directory: str) -> str:
        src = os.path.abspath(self.src_path)
        root = os.path.abspath(root_directory)
        dst = os.path.normpath(os.path.join(root, self.dst_url))
        if not os.path.isdir(root):
            raise NotADirectoryError(root)
        if not os.path.isfile(src):
            raise FileNotFoundError(src)
        if os.path.exists(dst):
            raise FileExistsError(dst)
        require_contained(dst, root=root)

        make_ancestors(dst)
        copyfile(src=src, dst=dst)
        return dst
