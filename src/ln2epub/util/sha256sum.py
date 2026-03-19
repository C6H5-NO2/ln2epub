from concurrent.futures import ThreadPoolExecutor
from hashlib import file_digest, sha256
from pathlib import Path


def hash_file(file: str | Path) -> str:
    with open(file, 'rb') as fp:
        digest = file_digest(fp, sha256)
        return digest.hexdigest()


def _hash_file_formatted(file: Path, *, cwd: Path) -> str:
    path = file.relative_to(cwd).as_posix()
    digest = hash_file(file)
    return f'{digest} *{path}'


def hash_directory(path: str, *, cwd: str = None) -> list[str]:
    path = Path(path).resolve()
    if not path.is_dir():
        raise NotADirectoryError(path)
    cwd = Path(cwd).resolve() if cwd else path
    files = [file for file in path.rglob('*') if file.is_file()]
    files.sort(key=lambda file: file.relative_to(cwd).as_posix())
    with ThreadPoolExecutor() as executor:
        digests = executor.map(lambda file: _hash_file_formatted(file, cwd=cwd), files)
        digests = list(digests)
        return digests
