from .default_segment_id import SegmentId
from ..util.frozendict import frozendict


class DefaultSegmentTitleProvider:
    def __init__(self):
        self._title_map: frozendict[str, str] = {
            SegmentId.COVER: '封面',
            SegmentId.TITLE: '標題',
            SegmentId.COPYRIGHT: '資訊',
            SegmentId.SUMMARY: '簡介',
            SegmentId.FOREWORD: '前言',
            SegmentId.ILLUSTRATION: '插圖',
            SegmentId.CONTENTS: '目錄',
            SegmentId.PROLOGUE: '序幕',
            SegmentId.CHAPTER_TEMPLATE: '第 {:d} 章',
            SegmentId.EPILOGUE: '尾聲',
            SegmentId.AFTERWORD: '後記',
            SegmentId.APPENDIX: '附錄',
            SegmentId.BACK: '封底',
        }

    def get_title(self, segment_id: str) -> str:
        if (chapter_index := SegmentId.get_chapter_index(segment_id)) is not None:
            title = self._get_chapter_title(chapter_index)
            return title
        title = self._title_map.get(segment_id, None)
        if not title:
            raise ValueError(f'title undefined for `{segment_id}`')
        return title

    def _get_chapter_title(self, chapter_index: int) -> str:
        title = self._title_map[SegmentId.CHAPTER_TEMPLATE]
        title = title.format(chapter_index)
        return title
