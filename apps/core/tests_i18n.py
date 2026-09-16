"""Language switcher: next URL must follow i18n_patterns prefixes."""

from django.conf import settings
from django.test import Client, SimpleTestCase
from django.urls import reverse

from apps.core.templatetags.rs_i18n import localize_path_for


class LocalizePathForTests(SimpleTestCase):
    def test_en_home_to_uk(self):
        self.assertEqual(localize_path_for('/en/', 'uk'), '/')

    def test_en_catalog_to_uk(self):
        self.assertEqual(localize_path_for('/en/catalog/', 'uk'), '/catalog/')

    def test_en_catalog_to_zh(self):
        self.assertEqual(localize_path_for('/en/catalog/', 'zh-hans'), '/zh-hans/catalog/')

    def test_uk_home_to_en(self):
        self.assertEqual(localize_path_for('/', 'en'), '/en/')

    def test_zh_to_uk_keeps_query(self):
        self.assertEqual(
            localize_path_for('/zh-hans/catalog/?q=cohiba', 'uk'),
            '/catalog/?q=cohiba',
        )

    def test_absolute_en_to_uk(self):
        self.assertEqual(
            localize_path_for('http://127.0.0.1:8000/en/catalog/', 'uk'),
            'http://127.0.0.1:8000/catalog/',
        )


class SetLanguageViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('set_language')

    def test_from_en_home_to_uk(self):
        response = self.client.post(self.url, {'language': 'uk', 'next': '/en/'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'uk')

    def test_from_en_catalog_to_zh(self):
        response = self.client.post(
            self.url, {'language': 'zh-hans', 'next': '/en/catalog/'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/zh-hans/catalog/')
        self.assertEqual(
            response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'zh-hans'
        )

    def test_from_uk_to_en(self):
        response = self.client.post(self.url, {'language': 'en', 'next': '/'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/en/')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')
