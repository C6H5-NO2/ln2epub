import re
from typing import final

from ..libxml.html import HtmlElement, html_element_maker
from ..libxml.xml import ElementMaker


class BrArticleNormaliser:
    def __init__(self, em: ElementMaker[HtmlElement] = None):
        self._em: ElementMaker[HtmlElement] = em if em is not None else html_element_maker()

    def normalise(self, article: HtmlElement) -> HtmlElement:
        target: HtmlElement = self._em.div()

        p: HtmlElement = self._em.p()
        if (text := self._normed_text(article)) is not None:
            p.text = text

        for child in article:
            child_tag = self._normed_tag(child)
            # todo: handle edge cases
            if child_tag == 'br':
                target.append(p)
                p = self._em.p()
                if (child_tail := self._normed_tail(child)) is not None:
                    p.text = child_tail
            else:
                self._norm(child, p)

        if p.getparent() is None:
            target.append(p)

        return target

    def _normed_tag(self, el: HtmlElement) -> str:
        tag = el.tag
        if not isinstance(tag, str):
            raise TypeError(f'element <{tag}> has tag of type {type(tag)}')
        if not tag:
            raise ValueError('element tag is empty')
        if tag[0] == '{':
            raise ValueError(f'element <{tag}> has namespaced tag')
        return tag

    def _normed_text(self, el: HtmlElement) -> str | None:
        text = el.text
        # keep text == ''
        if text is None:
            return None
        text = re.sub(r'\s+', ' ', text, flags=re.ASCII)
        # todo: should move this to subclass and only apply to br tail
        text = re.sub(r'^( ?)\u3000+', r'\1', text, count=1)
        return text

    def _normed_tail(self, el: HtmlElement) -> str | None:
        tail = el.tail
        if tail is None:
            return None
        el = self._em.span(tail)
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
        target: HtmlElement = self._em(tag)
        if attribs:
            for key in attribs:
                if (val := el.get(key)) is not None:
                    target.set(key, val)
        if text:
            if (t := self._normed_text(el)) is not None:
                target.text = t
        if tail:
            if (t := self._normed_tail(el)) is not None:
                target.tail = t
        if children:
            self._norm_children(el, target)
        if append:
            target_parent.append(target)
        return target

    def _norm_el_a(self, a: HtmlElement, target_parent: HtmlElement) -> None:
        self._norm_by_copy(a, target_parent, attribs=['href'])

    def _norm_el_b(self, b: HtmlElement, target_parent: HtmlElement) -> None:
        self._norm_by_copy(b, target_parent)

    def _norm_el_br(self, br: HtmlElement, target_parent: HtmlElement) -> None:
        if br.text:
            raise ValueError('<br> has text')
        if len(br) > 0:
            raise ValueError('<br> has children')
        # todo
        raise NotImplementedError()

    def _norm_el_img(self, img: HtmlElement, target_parent: HtmlElement) -> None:
        self._norm_by_copy(img, target_parent, attribs=['src'], text=False, children=False)

    def _norm_el_ruby(self, ruby: HtmlElement, target_parent: HtmlElement) -> None:
        target = self._norm_by_copy(ruby, None, tag='ruby', children=False, append=False)
        for child in ruby:
            match self._normed_tag(child):
                case 'rb' | 'rp' | 'rt' as tag:
                    target_rx = self._norm_by_copy(child, target, tag=tag)
                    if tag == 'rb':
                        # <rb> is deprecated
                        target_rx.drop_tag()
                case _:
                    self._norm(child, target)
        target_parent.append(target)
