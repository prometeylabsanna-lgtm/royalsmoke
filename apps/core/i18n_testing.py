"""Спільні перевірки тестів інтеграції ms / fil / id / vi (сторінки 02–10)."""

from __future__ import annotations

import json
import sys
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.utils.html import escape

from apps.core.i18n_audit import collect_texts, cyrillic_leftovers

SCRIPTS = Path(settings.BASE_DIR) / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from i18n_sea import DATA_DIR, SEA_LANGUAGES  # noqa: E402

# Рядки сторінок, які інтегруємо пізніше. Порожньо: обране ввійшло зі сторінкою 05.
PENDING_LATER_PAGES: tuple[str, ...] = ()

_WRAPPERS = ('a[title]', 'button[aria-label]', 'input[placeholder]', 'section[aria-label]', 'nav[aria-label]')


def page_strings(lang: str, page: str) -> dict[str, str]:
    path = DATA_DIR / lang / f'{page}.json'
    return json.loads(path.read_text(encoding='utf-8'))['strings']


def seed_storefront() -> None:
    """Демо-каталог + CMS і переклади, як на деплої (seed_demo → fill_i18n_content)."""
    out = StringIO()
    call_command('seed_demo', stdout=out)
    call_command('fill_i18n_content', stdout=out, stderr=out)


class TranslationPageMixin:
    """Для TestCase: _html(), _leftovers(), assert_phrases_rendered()."""

    def _html(self, path: str, *, adult: bool = True, **extra) -> str:
        if adult:
            self.client.cookies['age_ok'] = '1'
        else:
            self.client.cookies.pop('age_ok', None)
        response = self.client.get(path, **extra)
        self.assertEqual(response.status_code, 200, path)
        return response.content.decode()

    def _leftovers(self, html: str, mode: str = 'all') -> list[str]:
        return [
            text for text in cyrillic_leftovers(html, mode)
            if not any(pending in text for pending in PENDING_LATER_PAGES)
        ]

    def assert_no_cyrillic(self, path: str, **extra) -> None:
        for lang in SEA_LANGUAGES:
            self.assertEqual(self._leftovers(self._html(f'/{lang}{path}', **extra)), [], f'{lang} {path}')

    def assert_phrases_rendered(self, page: str, paths: list[str], *, minimum: int = 1, **extra) -> int:
        """Кожна фраза таблиці, видима на українській сторінці, присутня на перекладеній."""
        checked = 0
        for path in paths:
            uk_texts = set(collect_texts(self._html(path, **extra), 'all'))
            for lang in SEA_LANGUAGES:
                html = self._html(f'/{lang}{path}', **extra)
                for uk, tr in page_strings(lang, page).items():
                    visible = uk in uk_texts or any(f'{kind} {uk}' in uk_texts for kind in _WRAPPERS)
                    if not visible or '{' in uk or '%(' in uk:
                        continue
                    self.assertIn(escape(tr), html, f'{lang} {path}: {uk!r} -> {tr!r}')
                    checked += 1
        self.assertGreaterEqual(checked, minimum)
        return checked
