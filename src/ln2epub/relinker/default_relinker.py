import os.path
from mimetypes import guess_file_type
from urllib.parse import unquote, urlsplit

from .base_relinker import BaseRelinker
from ..libepub.expanded_epub import AUDIO, FONT, IMAGE, SCRIPT, STYLE, TEXT


class DefaultRelinker(BaseRelinker):
    def _replace_link(self, link, el, attrib, pos):
        link = link.strip('\u0020')
        if not link:
            raise ValueError('empty link')
        rst = urlsplit(link)
        if rst.scheme and rst.scheme != 'https':
            # raise when `http` is by design
            # link could be base64-encoded image data; truncate before logging
            raise ValueError(f'invalid scheme `{rst.scheme}` in link `{link[:64]}`')
        if not rst.path:
            # in most cases, a netloc-only url does not link to a resource
            raise ValueError(f'empty path in link `{link}`')
        rst = unquote(rst.path)
        rst = os.path.basename(rst)
        if not rst:
            raise ValueError(f'empty filename in link `{link}`')
        file_name = rst
        file_type, _ = guess_file_type(file_name)
        # todo
        match file_type:
            case None:
                raise NotImplementedError()

            case ft if ft.startswith('image/'):
                folder = IMAGE
                raise NotImplementedError()

            case 'application/xhtml+xml':
                folder = TEXT
                raise NotImplementedError()

            case 'text/css':
                folder = STYLE
                raise NotImplementedError()

            case 'application/javascript':
                folder = SCRIPT
                raise NotImplementedError()

            case ft if ft.startswith('audio/'):
                folder = AUDIO
                raise NotImplementedError()

            case ft if ft.startswith('font/'):
                folder = FONT
                raise NotImplementedError()

            case ft if ft.startswith('text/'):
                raise NotImplementedError()

            case ft if ft.startswith('video/'):
                raise NotImplementedError()

            case _:
                raise NotImplementedError()

        raise NotImplementedError()
