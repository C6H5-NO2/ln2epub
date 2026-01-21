import os.path
from dataclasses import dataclass
from shutil import copyfile

from ..util.path import contained_url


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerResourceBuilder:
    src_path: str
    dst_url: str
    root_directory: str

    def build(self) -> str:
        src = os.path.abspath(self.src_path)
        root = os.path.abspath(self.root_directory)
        dst = os.path.normpath(os.path.join(root, self.dst_url))
        if not os.path.isfile(src):
            raise FileNotFoundError(src)
        if os.path.exists(dst):
            raise FileExistsError(dst)
        if not contained_url(dst, root=root):
            raise PermissionError(dst)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        copyfile(src=src, dst=dst)
        return dst
