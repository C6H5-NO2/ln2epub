import os.path
from dataclasses import dataclass
from shutil import rmtree


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class WorkspaceStage:
    force: bool = True

    def run(
        self,
        *,
        workspace_directory: str,
    ) -> str:
        workspace_directory = os.path.abspath(workspace_directory)
        if not self.force and os.path.isdir(workspace_directory):
            print(f'reuse workspace `{workspace_directory}`')
            return workspace_directory
        if self.force:
            if os.path.isdir(workspace_directory):
                rmtree(workspace_directory, ignore_errors=False)
            elif os.path.isfile(workspace_directory):
                os.remove(workspace_directory)
        if os.path.exists(workspace_directory):
            raise FileExistsError(workspace_directory)
        os.makedirs(workspace_directory, exist_ok=False)
        print(f'built workspace `{workspace_directory}`')
        return workspace_directory
