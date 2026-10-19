"""Сторінка 07 «Про нас і FAQ»: переклади ms / fil / id / vi з docs/i18n/07-about-faq.md."""

from django.test import TestCase

from apps.core.i18n_testing import TranslationPageMixin, seed_storefront


class AboutFaqTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()

    def test_about_and_faq_have_no_cyrillic(self):
        for path in ('/about/', '/faq/'):
            self.assert_no_cyrillic(path)

    def test_faq_answers_are_translated(self):
        html = self._html('/vi/faq/')
        self.assertIn('Bảo quản xì gà như thế nào?', html)
        self.assertIn('đặt hàng với tư cách khách', html)
        self.assertNotIn('Як зберігати сигари', html)

    def test_about_story_is_translated(self):
        html = self._html('/vi/about/')
        self.assertIn('Câu chuyện của một quyết định', html)
        self.assertIn('Không gian đầu tiên', html)
        self.assertNotIn('Хроніка одного рішення', html)

    def test_table_phrases_are_rendered(self):
        self.assert_phrases_rendered('07-about-faq', ['/about/', '/faq/'], minimum=40)
