import subprocess
from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class EpubCheck:
    java: str = 'java'
    epubcheck: str = 'epubcheck.jar'
    root_directory: str

    def build(self):
        process = subprocess.run(
            args=[
                self.java,
                '-jar',
                self.epubcheck,
                self.root_directory,
                '--mode',
                'exp',
                # '--save',
            ],
            shell=False,
            capture_output=True,
            check=False,
            encoding='utf-8',
        )
        print(process.returncode)
        print(process.stdout)
        print(process.stderr)
