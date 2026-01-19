import os.path


def derive_relpath(
    *,
    path: str,
    root: str,
    strict_within: bool = True,
) -> str | None:
    path = os.path.abspath(path)
    root = os.path.abspath(root)
    try:
        common = os.path.commonpath([path, root])
        if common != root:
            return None
        rel = os.path.relpath(path, root)
        if strict_within and rel == '.':
            return None
        return rel.replace(os.path.sep, '/')
    except ValueError:
        return None
