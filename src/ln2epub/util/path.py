import os.path
import re
from typing import Literal


def contained_url(path: str, *, root: str, strict: bool = True) -> str | None:
    """
    :param path: Local file/directory path
    :param root: Local directory path
    :return: Contained url if so
    """
    path = os.path.abspath(path)
    root = os.path.abspath(root)
    try:
        common = os.path.commonpath([path, root])
        if common != root:
            return None
        rel = os.path.relpath(path, start=root)
        if strict and rel == '.':
            return None
        return rel.replace(os.path.sep, '/')
    except ValueError:
        return None


def require_contained(path: str, *, root: str) -> str:
    """
    :param path: Local file/directory path
    :param root: Local directory path
    :return: Contained url or raise
    """
    url = contained_url(path, root=root, strict=True)
    if not url:
        raise PermissionError(path)
    return url


def relative_url(
    path: str,
    *,
    start: str,
    root: str,
    mode: Literal['path', 'url'] = 'path',
) -> str | None:
    """
    :param path: Local file/directory path
    :param start: Local file path
    :param root: Local directory path
    :return: Relative url of `path` to `parent(start)` if so
    :param mode: If `url`, `path` and `start` are interpreted as url.
    """
    match mode:
        case 'path':
            pass

        case 'url':
            return relative_url(
                path=os.path.join(root, path),
                start=os.path.join(root, start),
                root=root,
                mode='path',
            )

        case _:
            raise ValueError(mode)
    path = contained_url(path, root=root, strict=False)
    start_dir = os.path.dirname(os.path.abspath(start))
    start_dir = contained_url(start_dir, root=root, strict=False)
    if path and start_dir:
        rel = os.path.relpath(path, start=start_dir)
        return rel.replace(os.path.sep, '/')
    return None


def make_ancestors(path: str) -> str:
    path = os.path.abspath(path)
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)
    return parent


def is_valid_filename(filename: str) -> bool:
    """
    This function is designed to be rather conservative.
    """
    if len(filename) not in range(1, 128):
        # technically, most filesystems (incl OCF) allow filenames less than 256 chars
        # however, `filename` often gets pre-/suffixes appended later so let's be conservative here
        return False
    if filename[-1] == '.':
        return False
    if '..' in filename:
        return False
    if re.fullmatch(r'(?:CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(?:\..*)?', filename, re.ASCII | re.IGNORECASE):
        # reserved filenames
        return False
    if not re.fullmatch(r'[\w\-.]+', filename, re.ASCII):
        # not "portable filename"
        return False
    return True


def is_valid_contained_url(url: str) -> bool:
    """
    This function is designed to be rather conservative.
    NB Only validates the format, NOT whether it is contained.
    """
    if len(url) not in range(1, 65536):
        return False
    if url[0] == '/':
        return False
    names = url.split('/')
    return all(name == '..' or is_valid_filename(name) for name in names)
