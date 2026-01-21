import os.path


def contained_path(
    path: str,
    *,
    root: str,
    strict: bool = True,
) -> str | None:
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


def relative_url_path(
    path: str,
    *,
    start: str,
    root: str
) -> str | None:
    path = contained_path(path, root=root, strict=False)
    start_dir = os.path.dirname(os.path.abspath(start))
    start_dir = contained_path(start_dir, root=root, strict=False)
    if path and start_dir:
        rel = os.path.relpath(path, start=start_dir)
        return rel.replace(os.path.sep, '/')
    return None
