"""Сторінка 02 «Головна»: переклади ms / fil / id / vi з docs/i18n/02-golovna.md."""

import json
import sys
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils.html import escape

from apps.core.i18n_audit import collect_texts, cyrillic_leftovers

SCRIPTS = Path(settings.BASE_DIR) / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from i18n_sea import DATA_DIR, SEA_LANGUAGES  # noqa: E402

# Рядки сторінок, які інтегруємо пізніше (картка товару: сторінка 05 «Акаунт»).
PENDING_LATER_PAGES = ('Додати до вибраного', 'Прибрати з вибраного')


def page_strings(lang, page='02-golovna'):
    path = DATA_DIR / lang / f'{page}.json'
    return json.loads(path.read_text(encoding='utf-8'))['strings']


class HomePageTranslationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        out = StringIO()
        call_command('seed_demo', stdout=out)
        call_command('fill_i18n_content', stdout=out, stderr=out)

    def _html(self, path):
        self.client.cookies['age_ok'] = '1'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, path)
        return response.content.decode()

    def _leftovers(self, html):
        return [
            text for text in cyrillic_leftovers(html, 'all')
            if not any(pending in text for pending in PENDING_LATER_PAGES)
        ]

    def test_brand_blurb_uses_table_when_language_column_empty(self):
        from apps.catalog.models_base import Brand
        from apps.core.models import HomeBrandCard

        card = HomeBrandCard.objects.select_related('brand').get(brand__slug='oliva')
        card.text_en = (
            'Deep profiles with cocoa, leather, and cedar — Oliva builds cigars '
            'for a long evening ritual.'
        )
        card.text_ind = ''
        card.save(update_fields=['text_en', 'text_ind'])
        brand = Brand.objects.get(slug='oliva')
        brand.short_description_ind = ''
        brand.save(update_fields=['short_description_ind'])

        html = self._html('/id/')
        self.assertIn('Oliva menciptakan cerutu', html)
        self.assertNotIn('Oliva builds cigars', html)

    def test_no_cyrillic_on_home_page(self):
        for lang in SEA_LANGUAGES:
            self.assertEqual(self._leftovers(self._html(f'/{lang}/')), [], lang)

    def test_every_table_phrase_visible_on_ukrainian_home_is_translated(self):
        uk_texts = set(collect_texts(self._html('/'), 'all'))
        # Фрази таблиці, що є на українській головній, мають бути на перекладеній.
        checked = 0
        for lang in SEA_LANGUAGES:
            html = self._html(f'/{lang}/')
            for uk, tr in page_strings(lang).items():
                visible = uk in uk_texts or any(text == f'{kind} {uk}' for text in uk_texts for kind in (
                    'a[title]', 'button[aria-label]', 'input[placeholder]', 'section[aria-label]',
                ))
                if not visible or '{{' in uk or '%(' in uk:
                    continue
                self.assertIn(escape(tr), html, f'{lang}: {uk!r} -> {tr!r}')
                checked += 1
        self.assertGreater(checked, 120)

    def test_prices_use_local_currency_symbols(self):
        expected = {'ms': 'RM', 'fil': '₱', 'id': 'Rp', 'vi': '₫'}
        for lang, symbol in expected.items():
            self.assertIn(symbol, self._html(f'/{lang}/'), lang)

    def test_zero_decimal_prices_have_no_fraction(self):
        import re

        for lang in ('id', 'vi'):
            html = self._html(f'/{lang}/')
            amounts = re.findall(r'rs-pcard__amount">([^<]+)<', html)
            self.assertTrue(amounts, lang)
            for amount in amounts:
                # Ціле число з групами розрядів (910.256), без дробової частини.
                self.assertRegex(amount.strip(), r'^\d{1,3}(?:[.,\u00a0\u202f ]\d{3})*$', (lang, amount))
