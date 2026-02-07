from ..libxml.html import HtmlElement


class CssPatternSelector:
    def __init__(self, css_selector: str):
        self._css_selector: str = css_selector

    def select_main(self, html: HtmlElement) -> HtmlElement:
        css_selector = self._css_selector
        el_list = html.cssselect(css_selector)
        if not el_list:
            raise ValueError(f'no match for css selector `{css_selector}`')
        return el_list[0]
