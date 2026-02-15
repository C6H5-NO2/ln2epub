import os.path
from mimetypes import guess_file_type
from urllib.parse import unquote, urlsplit

from .base_relinker import BaseRelinker
from ..libepub.consts import AUDIO, EPUB, FONT, IMAGE, SCRIPT, STYLE, TEXT
from ..util.path import relative_url


class DefaultRelinker(BaseRelinker):
    def _replace_link(self, link, el, attrib, pos):
        link = link.strip('\u0020')

        # parse filename
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

        # dispatch file by type into folder
        file_name = rst
        file_type, _ = guess_file_type(file_name)
        folder = 'misc'
        match file_type:
            case None:
                raise ValueError(f'unknown filetype of link `{link}`')

            case ft if ft.startswith('image/'):
                folder = IMAGE

            case 'application/xhtml+xml':
                folder = TEXT

            case 'text/css':
                folder = STYLE

            case 'application/javascript':
                folder = SCRIPT

            case ft if ft.startswith('audio/'):
                folder = AUDIO

            case ft if ft.startswith('font/'):
                folder = FONT

            case _:
                raise ValueError(f'unknown filetype `{file_type}` of link `{link}`')

        # todo: allow overriding
        dst_url = f'{EPUB}/{folder}/{file_name}'  # delegate the validation of this url to caller
        self_folder = f'{EPUB}/{TEXT}/'  # the default folder for xhtml files
        new_link = relative_url(dst_url, start=f'{self_folder}/.xhtml', root='./', mode='url')
        src_path = file_name  # prepend path outside
        return new_link, dst_url, src_path
