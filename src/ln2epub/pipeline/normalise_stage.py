import os.path
from dataclasses import dataclass

from ..libxml.html import html_parse
from ..libxml.xhtml import html_to_xhtml, xhtml_document, xhtml_dump, xhtml_parse, xhtml_to_html
from ..normaliser.normaliser import Normaliser
from ..normaliser.selector import Selector


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NormaliseStage:
    selector: Selector
    normaliser: Normaliser
    lang: str
    force: bool = True

    def run(
        self,
        *,
        html_path: str,
        normalised_xhtml_path: str,
    ) -> str:
        if not self.force and os.path.isfile(normalised_xhtml_path):
            print(f'reuse normalised `{normalised_xhtml_path}`')
            return normalised_xhtml_path

        if not os.path.isfile(html_path):
            raise FileNotFoundError(html_path)
        if html_path.endswith('.html') or html_path.endswith('.htm'):
            html_el = html_parse(html_path)
        elif html_path.endswith('.xhtml'):
            html_el = xhtml_parse(html_path)
        else:
            raise ValueError(html_path)
        xhtml_to_html(html_el)

        main_el = self.selector.select_main(html_el)
        normed_el = self.normaliser.normalise(main_el)

        html_to_xhtml(normed_el)
        normed_el = xhtml_document(normed_el, lang=self.lang)
        xhtml_dump(normed_el, normalised_xhtml_path)

        print(f'normalised to `{normalised_xhtml_path}`')
        return normalised_xhtml_path
