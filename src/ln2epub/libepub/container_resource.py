import os.path
from dataclasses import dataclass
from shutil import copyfile

from ..util.path import contained_path


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerResourceBuilder:
    src: str
    dst: str
    root: str

    def build(self) -> str:
        src = os.path.abspath(self.src)
        root = os.path.abspath(self.root)
        dst = os.path.normpath(os.path.join(root, self.dst))
        if not os.path.isfile(src):
            raise FileNotFoundError(src)
        if os.path.exists(dst):
            raise FileExistsError(dst)
        if not contained_path(dst, root=root):
            raise PermissionError(dst)

        copyfile(src=src, dst=dst)
        return dst
