import json
import os.path
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class EpubCheck:
    java: str = 'java'
    epubcheck: str = 'epubcheck.jar'
    root_directory: str
    strict: bool = True
    overwrite: bool = False

    def build(self) -> str:
        java = shutil.which(self.java)
        if not java:
            raise FileNotFoundError(self.java)
        epubcheck = os.path.abspath(self.epubcheck)
        if not os.path.isfile(epubcheck):
            raise FileNotFoundError(self.epubcheck)
        root_directory = os.path.abspath(self.root_directory)
        if not os.path.isdir(root_directory):
            raise NotADirectoryError(self.root_directory)
        output_path = f'{root_directory}.epub'
        if not self.overwrite and os.path.exists(output_path):
            raise FileExistsError(output_path)
        args: list[str] = [
            java,
            '-jar',
            epubcheck,
            root_directory,
            '--mode',
            'exp',
            '--save',
        ]
        if self.strict:
            args.append('--failonwarnings')
        process = subprocess.run(
            args=args,
            shell=False,
            capture_output=True,
            check=False,
            encoding='utf-8',
        )
        if process.returncode:
            msg = json.dumps(
                {
                    'stdout': process.stdout.splitlines(),
                    'stderr': process.stderr.splitlines(),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            raise RuntimeError(msg)
        return output_path
