import os.path
from dataclasses import dataclass
from shutil import rmtree


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class WorkspaceStage:
    force: bool = True

    def run(
        self,
        *,
        workspace_dir: str,
    ) -> str:
        workspace_dir = os.path.abspath(workspace_dir)
        if not self.force and os.path.isdir(workspace_dir):
            print(f'reuse workspace `{workspace_dir}`')
            return workspace_dir
        if self.force:
            if os.path.isdir(workspace_dir):
                rmtree(workspace_dir, ignore_errors=False)
            elif os.path.isfile(workspace_dir):
                os.remove(workspace_dir)
        if os.path.exists(workspace_dir):
            raise FileExistsError(workspace_dir)
        os.makedirs(workspace_dir, exist_ok=False)
        print(f'built workspace `{workspace_dir}`')
        return workspace_dir
