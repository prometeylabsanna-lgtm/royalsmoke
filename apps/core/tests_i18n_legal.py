"""Сторінка 09 «Юридичні»: переклади ms / fil / id / vi з docs/i18n/09-legal.md."""

from django.test import TestCase

from apps.core.i18n_testing import SEA_LANGUAGES, TranslationPageMixin, seed_storefront

PATHS = (
    '/service/delivery/',
    '/legal/privacy/',
    '/legal/terms/',
    '/legal/age/',
    '/legal/cookies/',
)


class LegalTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()

    def test_pages_have_no_cyrillic(self):
        for path in PATHS:
            self.assert_no_cyrillic(path)

    def test_privacy_and_delivery_keep_structure(self):
        for lang in SEA_LANGUAGES:
            privacy = self._html(f'/{lang}/legal/privacy/')
            self.assertIn('<h2>1.', privacy)
            self.assertIn('Nova Poshta', privacy)
            self.assertNotIn('Нова Пошта', privacy)
            delivery = self._html(f'/{lang}/service/delivery/')
            self.assertIn('Nova Poshta', delivery)
            self.assertNotIn('Київ', delivery)

    def test_vietnamese_headings(self):
        self.assertIn('Chính sách bảo mật', self._html('/vi/legal/privacy/'))
        self.assertIn('Giao hàng và thanh toán', self._html('/vi/service/delivery/'))
        self.assertIn('Điều khoản sử dụng', self._html('/vi/legal/terms/'))

    def test_table_phrases_are_rendered(self):
        self.assert_phrases_rendered('09-legal', list(PATHS), minimum=40)
