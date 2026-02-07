import re
from typing import final

from ..libxml.html import HtmlElement, html_element_maker
from ..libxml.xhtml import XHTML_NAMESPACE
from ..libxml.xml import ElementMaker, get_text_tail, set_text_tail, unwrap_sole_child


class BrArticleNormaliser:
    def __init__(self, em: ElementMaker[HtmlElement] = None):
        self._em: ElementMaker[HtmlElement] = em if em is not None else html_element_maker()

    def normalise(self, article: HtmlElement) -> HtmlElement:
        div: HtmlElement = self._em.div()

        p = self._em.p()
        if (text := self._normed_text(article)) is not None:
            p.text = text

        for child in article:
            match self._normed_tag(child):
                case 'br':
                    self._norm_line(p, div)
                    p = self._em.p()
                    if (child_tail := self._normed_tail(child)) is not None:
                        p.text = child_tail

                case _:
                    self._norm(child, p)

        self._norm_line(p, div)

        return div

    def _normed_tag(self, el: HtmlElement) -> str:
        tag = el.tag
        if not isinstance(tag, str):
            raise TypeError(f'element <{tag}> has tag of type {type(tag)}')
        if not tag:
            raise ValueError('element has empty tag')
        if tag[0] == '{':
            if len(tag) > len(XHTML_NAMESPACE) + 2 and tag.startswith(f'{{{XHTML_NAMESPACE}}}'):
                return tag[len(XHTML_NAMESPACE) + 2:]
            else:
                raise ValueError(f'element <{tag}> has namespaced tag')
        return tag

    def _normed_text(self, el: HtmlElement) -> str | None:
        text = el.text
        # keep text == ''
        if text is None or text == '':
            return text
        text = re.sub(r'\s+', '\u0020', text, flags=re.ASCII)
        return text

    def _normed_tail(self, el: HtmlElement) -> str | None:
        tail = el.tail
        if tail is None or tail == '':
            return tail
        el = self._em(el.tag, tail)
        return self._normed_text(el)

    def _norm(self, el: HtmlElement, target_parent: HtmlElement) -> None:
        tag = self._normed_tag(el)
        func = getattr(self, f'_norm_el_{tag}', None)
        if not callable(func):
            self._norm_unknown(el, target_parent)
            return
        func(el, target_parent)

    def _norm_children(self, el: HtmlElement, target_parent: HtmlElement) -> None:
        for child in el:
            self._norm(child, target_parent)

    def _norm_unknown(self, el: HtmlElement, target_parent: HtmlElement) -> None:
        raise ValueError(f'unknown element <{el.tag}>')

    def _norm_line(self, line: HtmlElement, target_parent: HtmlElement) -> None:
        assert line.getparent() is None
        assert line.tail is None

        # strip leading and trailing whitespace in direct text content of <line>
        whitespace = '\u0020\u00a0\u3000'
        if text := line.text:
            text = text.lstrip(whitespace)
            line.text = text
        if text_tail := get_text_tail(line):
            text_tail = text_tail.rstrip(whitespace)
            set_text_tail(line, text_tail)

        # empty line -> <p><br></p>
        # should use CSS `margin` instead
        if not line.text and not len(line):
            br = self._em.br()
            # merge <br> if possible
            if len(target_parent):
                prev = target_parent[-1]
                if not prev.text and len(prev) and all(self._normed_tag(ch) == 'br' for ch in prev):
                    prev.append(br)
                    return
            line.text = ''  # force '' to make it single line
            line.append(br)
            target_parent.append(line)
            return

        # promote single-line <span><img></span> into direct <div><img></div>
        if (imgs := line.cssselect('span > img[src][alt]')) and len(imgs) == 1:
            span = unwrap_sole_child(line)
            img = unwrap_sole_child(span)
            if img is not None and img == imgs[0]:
                line.remove(span)
                span.tag = 'div'
                span.tail = None  # force None to allow line break
                target_parent.append(span)
                return

        target_parent.append(line)

    @final
    def _norm_by_copy(
        self,
        el: HtmlElement,
        target_parent: HtmlElement | None,
        *,
        tag: str = None,
        attribs: list[str] = None,
        text: bool = True,
        tail: bool = True,
        children: bool = True,
        append: bool = True,
    ) -> HtmlElement:
        tag = tag if tag else self._normed_tag(el)
        normed: HtmlElement = self._em(tag)
        if attribs:
            for key in attribs:
                if (val := el.get(key)) is not None:
                    normed.set(key, val)
        if text:
            if (t := self._normed_text(el)) is not None:
                normed.text = t
        if tail:
            if (t := self._normed_tail(el)) is not None:
                normed.tail = t
        if children:
            self._norm_children(el, normed)
        if append:
            target_parent.append(normed)
        return normed

    def _norm_el_a(self, a: HtmlElement, target_parent: HtmlElement) -> None:
        self._norm_by_copy(a, target_parent, attribs=['href'])

    def _norm_el_b(self, b: HtmlElement, target_parent: HtmlElement) -> None:
        self._norm_by_copy(b, target_parent)

    def _norm_el_br(self, br: HtmlElement, target_parent: HtmlElement) -> None:
        # self._norm_by_copy(br, target_parent, text=False, children=False)
        raise ValueError('nested <br>')

    def _norm_el_img(self, img: HtmlElement, target_parent: HtmlElement) -> None:
        normed_img = self._norm_by_copy(img, None, attribs=['src', 'alt'], text=False, children=False, append=False)
        if normed_img.get('alt') is None:
            # force `alt` to hint downstream
            normed_img.set('alt', img.get('src'))
        span = self._em.span(normed_img)
        span.tail = normed_img.tail
        normed_img.tail = None
        target_parent.append(span)

    def _norm_el_ruby(self, ruby: HtmlElement, target_parent: HtmlElement) -> None:
        normed_ruby = self._norm_by_copy(ruby, None, children=False, append=False)
        for child in ruby:
            match self._normed_tag(child):
                case 'rb' | 'rp' | 'rt' as tag:
                    normed_rx = self._norm_by_copy(child, normed_ruby, tag=tag)
                    if tag == 'rb':
                        # <rb> is deprecated
                        normed_rx.drop_tag()
                case _:
                    self._norm(child, normed_ruby)
        target_parent.append(normed_ruby)
