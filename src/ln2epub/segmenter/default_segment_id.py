import re
from enum import StrEnum


class SegmentId(StrEnum):
    COVER = 'cover'
    TITLE = 'title'
    COPYRIGHT = 'copyright'
    SUMMARY = 'summary'
    FOREWORD = 'foreword'
    ILLUSTRATION = 'illustration'
    CONTENTS = 'contents'
    PROLOGUE = 'prologue'
    CHAPTER_TEMPLATE = 'chapter_{:02d}'
    EPILOGUE = 'epilogue'
    AFTERWORD = 'afterword'
    APPENDIX = 'appendix'
    BACK = 'back'

    @staticmethod
    def get_chapter_index(segment_id: str) -> int | None:
        if not re.fullmatch(r'chapter_\d+', segment_id, re.ASCII):
            return None
        chapter_idx = segment_id.removeprefix('chapter_')
        return int(chapter_idx)
