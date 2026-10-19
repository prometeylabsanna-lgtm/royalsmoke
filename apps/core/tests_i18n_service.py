"""Сторінка 06: бронювання, калькулятор, контакти, B2B — ms / fil / id / vi."""

from django.test import TestCase

from apps.core.i18n_testing import SEA_LANGUAGES, TranslationPageMixin, seed_storefront


class ServiceTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()

    def test_pages_have_no_cyrillic(self):
        for path in ('/booking/', '/service/contact/'):
            self.assert_no_cyrillic(path)

    def test_calculator_results_are_translated(self):
        for lang in SEA_LANGUAGES:
            html = self._html(
                f'/{lang}/calculator/results/',
                data={'strength': 'medium', 'format': 'robusto'},
                HTTP_HX_REQUEST='true',
            )
            self.assertNotIn('Переглянути', html, lang)
            self.assertNotIn('Ваші рекомендації', html, lang)
            self.assertEqual(self._leftovers(html), [], lang)

    def test_booking_slots_partial_is_translated(self):
        for lang in SEA_LANGUAGES:
            html = self._html(f'/{lang}/booking/slots/')
            self.assertNotIn('Оберіть послугу та дату', html, lang)
            self.assertEqual(self._leftovers(html), [], lang)

    def test_contact_validation_is_translated(self):
        for lang in SEA_LANGUAGES:
            response = self.client.post(f'/{lang}/service/contact/', {'name': 'An', 'message': ''})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self._leftovers(response.content.decode()), [], lang)

    def test_home_booking_text_is_not_english_fallback(self):
        html = self._html('/vi/')
        self.assertNotIn('Leave your contacts', html)
        self.assertIn('Hãy để lại thông tin liên hệ', html)

    def test_table_phrases_are_rendered(self):
        self.assert_phrases_rendered(
            '06-servis',
            ['/booking/', '/service/contact/', '/'],
            minimum=40,
        )
