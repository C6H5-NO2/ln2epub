from typing import Protocol


class SegmentTitleProvider(Protocol):
    def get_title(self, segment_id: str) -> str:
        ...
