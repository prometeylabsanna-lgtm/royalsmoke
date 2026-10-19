"""Сторінка 05 «Акаунт»: переклади ms / fil / id / vi з docs/i18n/05-akaunt.md."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.catalog.models import Product
from apps.core.i18n_testing import SEA_LANGUAGES, TranslationPageMixin, seed_storefront

User = get_user_model()
PASSWORD = 'Secret123!'


class AccountTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()
        cls.product = Product.objects.filter(is_active=True).first()
        cls.user = User.objects.create_user(
            email='sea@example.com', password=PASSWORD, first_name='Nguyen',
        )

    def _login(self, lang):
        self.client.cookies['age_ok'] = '1'
        logged = self.client.post(f'/{lang}/account/login/', {
            'username': 'sea@example.com',
            'password': PASSWORD,
        })
        self.assertEqual(logged.status_code, 302, lang)

    def test_guest_pages_have_no_cyrillic(self):
        for lang in SEA_LANGUAGES:
            for path in ('/account/login/', '/account/register/', '/wishlist/'):
                self.assert_no_cyrillic(path)

    def test_register_errors_have_no_cyrillic(self):
        for lang in SEA_LANGUAGES:
            html = self.client.post(f'/{lang}/account/register/', {
                'email': 'not-an-email',
                'password1': 'short',
                'password2': 'other',
                'age_confirm': '',
            })
            self.assertEqual(html.status_code, 200)
            self.assertEqual(self._leftovers(html.content.decode()), [], lang)

    def test_login_error_uses_filipino_django_catalog(self):
        self.client.cookies['age_ok'] = '1'
        response = self.client.post('/fil/account/login/', {
            'username': 'sea@example.com',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        text = response.content.decode()
        self.assertIn('Maglagay ng tamang', text)
        self.assertEqual(self._leftovers(text), [])

    def test_signed_in_pages_have_no_cyrillic(self):
        for lang in SEA_LANGUAGES:
            self._login(lang)
            self.client.post(f'/{lang}/wishlist/toggle/', {'product_id': self.product.id})
            for path in ('/account/cabinet/', '/account/password/', '/account/delete/', '/wishlist/'):
                self.assert_no_cyrillic(path)
            self.client.post(f'/{lang}/account/logout/')

    def test_password_mismatch_is_translated(self):
        for lang in SEA_LANGUAGES:
            self._login(lang)
            response = self.client.post(f'/{lang}/account/password/', {
                'old_password': PASSWORD,
                'new_password1': 'NewSecret123!',
                'new_password2': 'NewSecret456!',
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self._leftovers(response.content.decode()), [], lang)
            self.client.post(f'/{lang}/account/logout/')

    def test_table_phrases_are_rendered(self):
        self.client.cookies['age_ok'] = '1'
        self.assert_phrases_rendered(
            '05-akaunt',
            ['/account/login/', '/account/register/', '/wishlist/'],
            minimum=40,
        )
