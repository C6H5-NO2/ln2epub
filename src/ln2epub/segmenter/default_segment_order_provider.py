from .default_segment_id import SegmentId
from ..util.frozenlist import frozenlist


class DefaultSegmentOrderProvider:
    def __init__(self, *, chapters: range):
        self._chapters: range = chapters
        self._order_list: frozenlist[str] = [
            SegmentId.COVER,
            SegmentId.TITLE,
            SegmentId.COPYRIGHT,
            SegmentId.SUMMARY,
            SegmentId.FOREWORD,
            SegmentId.ILLUSTRATION,
            SegmentId.CONTENTS,
            SegmentId.PROLOGUE,
            SegmentId.CHAPTER_TEMPLATE,
            SegmentId.EPILOGUE,
            SegmentId.AFTERWORD,
            SegmentId.APPENDIX,
            SegmentId.BACK,
        ]

    def get_order(self, segment_id: str) -> int:
        index_chapter = self._order_list.index(SegmentId.CHAPTER_TEMPLATE)
        if (chapter_idx := SegmentId.get_chapter_index(segment_id)) is not None:
            index = index_chapter
            offset = chapter_idx - self._chapters.start
            return index + offset
        index = self._order_list.index(segment_id)
        offset = 0 if index < index_chapter else len(self._chapters) - 1
        return index + offset
