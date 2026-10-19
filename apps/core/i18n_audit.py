"""Аудит видимого тексту сторінки: де лишилась кирилиця (для мов без українського інтерфейсу).

Використовується в тестах інтеграції ms / fil / id / vi: сторінка іншою мовою не має
містити українських слів ні в тексті, ні в aria-label / title / alt / placeholder, ні в
meta-тегах і JSON-повідомленнях валідації.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

CYRILLIC = re.compile('[а-яіїєґА-ЯІЇЄҐ]')
VOID_TAGS = frozenset(
    {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
)
TEXT_ATTRS = ('aria-label', 'title', 'alt', 'placeholder')
META_KEYS = ('description', 'og:title', 'og:description', 'og:site_name', 'twitter:title', 'twitter:description')
JSON_SCRIPT_IDS = frozenset({'rs-i18n-validate'})
# Рідні назви мов у перемикачі: користувач має впізнати свою мову й повернутися на українську.
ALLOWED_NATIVE_NAMES = ('Українська',)


class _Collector(HTMLParser):
    """mode='chrome': усе поза <main> + хлібні крихти; mode='main': лише вміст <main>; 'all': усе."""

    def __init__(self, mode: str):
        super().__init__(convert_charrefs=True)
        self.mode = mode
        self.stack: list[tuple[str, bool]] = []
        self.items: list[str] = []
        self.in_title = False
        self.json_script = False

    # --- вибір області ---------------------------------------------------
    def _in_main(self) -> bool:
        return any(tag == 'main' for tag, _ in self.stack)

    def _in_crumbs(self) -> bool:
        return any(flag for _, flag in self.stack)

    def _active(self) -> bool:
        if self.mode == 'all':
            return True
        if self.mode == 'main':
            return self._in_main()
        return not self._in_main() or self._in_crumbs()

    # --- розбір ------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == 'meta':
            key = attr.get('name') or attr.get('property') or ''
            if key in META_KEYS and attr.get('content'):
                self.items.append(f'meta[{key}] {attr["content"]}')
            return
        if tag in VOID_TAGS:
            if self._active():
                self._collect_attrs(tag, attr)
            return
        classes = (attr.get('class') or '').split()
        self.stack.append((tag, 'rs-crumbs' in classes))
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attr.get('id') in JSON_SCRIPT_IDS:
            self.json_script = True
        if self._active():
            self._collect_attrs(tag, attr)

    def _collect_attrs(self, tag, attr):
        for name in TEXT_ATTRS:
            if attr.get(name):
                self.items.append(f'{tag}[{name}] {attr[name]}')
        if tag == 'input' and attr.get('type') in {'submit', 'button'} and attr.get('value'):
            self.items.append(f'input[value] {attr["value"]}')

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.json_script = False

    def handle_data(self, data):
        text = ' '.join(data.split())
        if not text:
            return
        if self.json_script:
            self.items.append(f'json[rs-i18n-validate] {text}')
            return
        if self.in_title:
            self.items.append(f'title {text}')
            return
        if any(tag in {'script', 'style'} for tag, _ in self.stack):
            return
        if self._active():
            self.items.append(text)


def collect_texts(html: str, mode: str = 'chrome') -> list[str]:
    collector = _Collector(mode)
    collector.feed(html)
    collector.close()
    return collector.items


def cyrillic_leftovers(html: str, mode: str = 'chrome') -> list[str]:
    """Фрагменти видимого тексту, у яких є кирилиця."""
    result = []
    for text in collect_texts(html, mode):
        cleaned = text
        for name in ALLOWED_NATIVE_NAMES:
            cleaned = cleaned.replace(name, '')
        if CYRILLIC.search(cleaned):
            result.append(text)
    return result
