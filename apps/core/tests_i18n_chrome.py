"""Сторінка 01 «Хром сайту»: шапка, футер, age gate, хлібні крихти, мета-теги, валідація."""

import sys
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils.html import escape

from apps.core.i18n_audit import collect_texts, cyrillic_leftovers
from apps.core.validation.rules import validate_name

SEA = ('ms', 'fil', 'id', 'vi')

SCRIPTS = Path(settings.BASE_DIR) / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from i18n_sea import load_language  # noqa: E402


def sea_text(lang, uk):
    """Переклад зі словника scripts/i18n_data (джерело — docs/i18n/01-khrom.md)."""
    return load_language(lang)[0][uk]


class ChromeTranslationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        out = StringIO()
        call_command('seed_demo', stdout=out)
        call_command('fill_i18n_content', stdout=out, stderr=out)

    def _page(self, path, *, adult=True):
        if adult:
            self.client.cookies['age_ok'] = '1'
        else:
            self.client.cookies.pop('age_ok', None)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, path)
        return response.content.decode()

    def test_no_cyrillic_in_chrome_with_age_gate(self):
        for lang in SEA:
            html = self._page(f'/{lang}/', adult=False)
            self.assertEqual(cyrillic_leftovers(html, 'chrome'), [], lang)

    def test_no_cyrillic_in_chrome_after_age_confirmation(self):
        for lang in SEA:
            for path in (f'/{lang}/', f'/{lang}/catalog/', f'/{lang}/service/contact/'):
                html = self._page(path)
                self.assertEqual(cyrillic_leftovers(html, 'chrome'), [], path)

    def test_validation_messages_json_is_translated(self):
        for lang in SEA:
            html = self._page(f'/{lang}/')
            payload = [t for t in collect_texts(html, 'chrome') if t.startswith('json[rs-i18n-validate]')]
            self.assertEqual(len(payload), 1, lang)
            self.assertIn('"required"', payload[0])

    def test_document_language_and_title(self):
        for lang in SEA:
            html = self._page(f'/{lang}/')
            self.assertIn(f'<html lang="{lang}">', html)

    def test_age_gate_and_footer_use_loaded_translations(self):
        for lang in SEA:
            gate = self._page(f'/{lang}/', adult=False)
            self.assertIn(escape(sea_text(lang, 'Вам виповнилося 21 рік?')), gate, lang)
            self.assertIn(escape(sea_text(lang, 'Мені є 21 рік')), gate, lang)
            home = self._page(f'/{lang}/')
            self.assertIn(escape(sea_text(lang, 'FAQ')), home, lang)
            self.assertIn(escape(sea_text(lang, 'Навігація футера')), home, lang)

    def test_breadcrumbs_translated_on_inner_pages(self):
        for lang in SEA:
            html = self._page(f'/{lang}/catalog/')
            self.assertIn('class="rs-crumbs"', html)
            self.assertIn(escape(sea_text(lang, 'Навігаційний шлях')), html, lang)
            self.assertEqual(cyrillic_leftovers(html, 'chrome'), [], lang)


class NameValidationScriptsTests(TestCase):
    def test_names_in_any_script_are_valid(self):
        for name in ('Nguyễn Văn An', 'Trần Thị Bích', 'Juan Dela Cruz', 'Niño', 'Nurul Aina binti Ahmad',
                     'Siti Nur Azizah', '王伟', 'Іван-Петро', "O'Brien", 'Anh'):
            self.assertIsNone(validate_name(name), name)

    def test_digits_and_symbols_are_rejected(self):
        for name in ('Anna2', 'Bob_x', 'x@y', 'A1', '12'):
            self.assertIsNotNone(validate_name(name), name)

    def test_decomposed_vietnamese_marks_are_accepted(self):
        decomposed = 'Nguye\u0302\u0303n Va\u0306n'
        self.assertIsNone(validate_name(decomposed))
