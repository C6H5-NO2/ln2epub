from mimetypes import guess_file_type
from os.path import basename
from urllib.parse import unquote, urlsplit

from .abstract_relinker import AbstractRelinker
from ..libepub.consts import AUDIO, EPUB, FONT, IMAGE, SCRIPT, STYLE, TEXT
from ..util.path import relative_url


class DefaultRelinker(AbstractRelinker):
    def _replace_link(self, el, attrib, link, pos):
        link = link.strip('\u0020')

        file_name = self._get_file_name(el=el, attrib=attrib, link=link, pos=pos)

        src_path = self._get_src_path(file_name, el=el, attrib=attrib, link=link, pos=pos)

        # dispatch file by type into folder
        dst_url = self._get_dst_url(file_name, el=el, attrib=attrib, link=link, pos=pos)

        new_link = self._get_new_link(dst_url, el=el, attrib=attrib, link=link, pos=pos)

        return new_link, dst_url, src_path

    def _get_file_name(self, el, attrib, link, pos) -> str:
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
        rst = basename(rst)
        if not rst:
            raise ValueError(f'empty filename in link `{link}`')
        return rst

    def _get_new_link(self, dst_url: str, el, attrib, link, pos) -> str:
        # default url for xhtml files
        self_url = f'{EPUB}/{TEXT}/xhtml.xhtml'
        new_link = relative_url(dst_url, start=self_url, root='./', mode='url')
        return new_link

    def _get_dst_url(self, file_name: str, el, attrib, link, pos) -> str:
        file_type, _ = guess_file_type(file_name)

        folder = 'misc'
        match file_type:
            case None:
                raise ValueError(f'unknown filetype of filename `{file_name}`')

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
                raise ValueError(f'unexpected filetype `{file_type}` of filename `{file_name}`')

        # delegate validation to outside
        # an `_` is added intentionally
        dst_url = f'{EPUB}/{folder}/_{file_name}'
        return dst_url

    def _get_src_path(self, file_name: str, el, attrib, link, pos) -> str:
        # prepend path outside
        return file_name
