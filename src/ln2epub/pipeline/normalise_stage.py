import os.path
from dataclasses import dataclass

from ..libxml.html import html_parse
from ..libxml.xhtml import html_to_xhtml, xhtml_document, xhtml_dump, xhtml_parse
from ..normaliser.normaliser import Normaliser
from ..normaliser.selector import Selector


@dataclass(eq=False, order=False, frozen=True, match_args=False, kw_only=True)
class NormaliseStage:
    html_path: str
    lang: str
    selector: Selector
    normaliser: Normaliser
    force: bool = True

    def run(
        self,
        *,
        normalised_xhtml_path: str,
    ) -> str:
        if not self.force and os.path.isfile(normalised_xhtml_path):
            print(f'reuse normalised `{normalised_xhtml_path}`')
            return normalised_xhtml_path

        if not os.path.isfile(self.html_path):
            raise FileNotFoundError(self.html_path)
        if self.html_path.endswith('.html'):
            html_el = html_parse(self.html_path)
        elif self.html_path.endswith('.xhtml'):
            html_el = xhtml_parse(self.html_path)
        else:
            raise ValueError(self.html_path)

        main_el = self.selector.select_main(html_el)
        normed_el = self.normaliser.normalise(main_el)
        html_to_xhtml(normed_el)
        normed_el = xhtml_document(normed_el, lang=self.lang)
        xhtml_dump(normed_el, normalised_xhtml_path)

        print(f'normalised to `{normalised_xhtml_path}`')
        return normalised_xhtml_path
