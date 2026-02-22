from typing import Protocol


class SegmentOrderProvider(Protocol):
    def get_order(self, segment_id: str) -> int | None:
        ...
