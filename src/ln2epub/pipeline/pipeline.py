from dataclasses import dataclass


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class Pipeline:
    workspace: str


    def build(self) -> str:
        pass
