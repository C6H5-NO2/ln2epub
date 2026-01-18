import os.path
from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class ContainerBuilder:
    root_directory: str


def build_container(arg: ContainerBuilder) -> str:
    root_dir = os.path.abspath(arg.root_directory)
    if os.path.exists(root_dir):
        raise FileExistsError(root_dir)
    os.makedirs(root_dir)

    mimetype = os.path.join(root_dir, 'mimetype')
    with open(mimetype, 'wt', encoding='ascii', newline='\n') as fp:
        fp.write('application/epub+zip')

    metainf_dir = os.path.join(root_dir, 'META-INF')
    os.makedirs(metainf_dir)

    return root_dir
