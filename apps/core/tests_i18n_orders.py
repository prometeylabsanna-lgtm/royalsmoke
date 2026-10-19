"""Сторінка 04 «Кошик і замовлення»: переклади ms / fil / id / vi з docs/i18n/04-zamovlennia.md."""

from decimal import Decimal

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Product
from apps.core.currency import language_currency_code
from apps.core.i18n_audit import cyrillic_leftovers
from apps.core.i18n_testing import (
    PENDING_LATER_PAGES,
    SEA_LANGUAGES,
    TranslationPageMixin,
    seed_storefront,
)
from apps.orders.models import Order


def _checkout_payload(token, **overrides):
    payload = {
        'first_name': 'Nguyễn',
        'last_name': 'Văn An',
        'phone': '+84901234567',
        'email': 'buyer@example.com',
        'delivery_service': 'pickup',
        'delivery_city': 'Kyiv',
        'delivery_address': 'Showroom',
        'payment_method': 'online',
        'age_confirm': '1',
        'checkout_token': token,
    }
    payload.update(overrides)
    return payload


@override_settings(DEMO_PAYMENTS=True, NOVA_POSHTA_API_KEY='')
class OrderFlowTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()
        cls.product = Product.objects.filter(is_active=True, stock__gt=5).first()

    def _client(self):
        client = Client()
        client.cookies['age_ok'] = '1'
        return client

    def _leftovers_of(self, response):
        return [
            text for text in cyrillic_leftovers(response.content.decode(), 'all')
            if not any(pending in text for pending in PENDING_LATER_PAGES)
        ]

    def _fill_cart(self, client, lang, quantity=1):
        return client.post(f'/{lang}/cart/add/', {'product_id': self.product.id, 'quantity': quantity})

    def test_empty_cart_and_cart_page(self):
        for lang in SEA_LANGUAGES:
            client = self._client()
            response = client.get(f'/{lang}/cart/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self._leftovers_of(response), [], f'{lang} empty cart')
            self._fill_cart(client, lang, 2)
            response = client.get(f'/{lang}/cart/')
            self.assertEqual(self._leftovers_of(response), [], f'{lang} cart')

    def test_checkout_page_and_validation_errors(self):
        for lang in SEA_LANGUAGES:
            client = self._client()
            self._fill_cart(client, lang)
            page = client.get(f'/{lang}/orders/checkout/')
            self.assertEqual(page.status_code, 200)
            self.assertEqual(self._leftovers_of(page), [], f'{lang} checkout')
            token = page.context['checkout_token']
            bad = client.post(f'/{lang}/orders/checkout/', _checkout_payload(
                token, first_name='', phone='x', email='nope', age_confirm='',
            ))
            self.assertEqual(bad.status_code, 200)
            self.assertEqual(self._leftovers_of(bad), [], f'{lang} checkout errors')
            nova = client.post(f'/{lang}/orders/checkout/', _checkout_payload(
                token, delivery_service='nova_poshta', delivery_address='',
            ))
            self.assertEqual(self._leftovers_of(nova), [], f'{lang} nova poshta error')

    def test_full_order_flow_pay_and_thank_you(self):
        for lang in SEA_LANGUAGES:
            client = self._client()
            self._fill_cart(client, lang)
            token = client.get(f'/{lang}/orders/checkout/').context['checkout_token']
            created = client.post(f'/{lang}/orders/checkout/', _checkout_payload(token))
            self.assertEqual(created.status_code, 302, lang)
            order = Order.objects.order_by('-pk').first()
            self.assertEqual(order.currency, language_currency_code(lang), lang)
            pay = client.get(created.url)
            self.assertEqual(pay.status_code, 200)
            self.assertEqual(self._leftovers_of(pay), [], f'{lang} pay page')
            ok = client.post(reverse('orders:demo_pay', args=[order.order_number]), {'outcome': 'success'},
                             follow=False)
            self.assertEqual(ok.status_code, 302)
            thank = client.get(ok.url)
            self.assertEqual(thank.status_code, 200)
            self.assertEqual(self._leftovers_of(thank), [], f'{lang} thank you')

    def test_order_totals_use_local_currency_precision(self):
        for lang in ('id', 'vi', 'ms'):
            client = self._client()
            self._fill_cart(client, lang, 3)
            token = client.get(f'/{lang}/orders/checkout/').context['checkout_token']
            client.post(f'/{lang}/orders/checkout/', _checkout_payload(token, payment_method='cod'))
            order = Order.objects.order_by('-pk').first()
            code = language_currency_code(lang)
            self.assertEqual(order.currency, code)
            self.assertGreater(order.fx_rate, 0)
            if code in ('IDR', 'VND'):
                for value in (order.subtotal, order.delivery_cost, order.total):
                    self.assertEqual(value, value.to_integral_value(), (lang, value))
            self.assertEqual(order.total, order.subtotal + order.delivery_cost - order.discount)
            self.assertGreater(order.total, Decimal('0'))
            self.assertEqual(
                order.fx_rate.as_tuple().exponent, -8, 'fx_rate stored with 8 decimal places',
            )

    def test_stock_limit_messages_translated(self):
        for lang in SEA_LANGUAGES:
            client = self._client()
            response = self._fill_cart(client, lang, 9999)
            cart = client.get(f'/{lang}/cart/')
            self.assertEqual(self._leftovers_of(cart), [], f'{lang} stock cart')
            self.assertIn(response.status_code, (200, 302, 400))

    def test_nova_poshta_partials_translated(self):
        # Назви міст і відділень приходять з API Нової Пошти українською — це дані, а не інтерфейс.
        # Перевіряємо службові тексти порожніх відповідей.
        for lang in SEA_LANGUAGES:
            client = self._client()
            cities = client.get(f'/{lang}/orders/np/cities/', {'q': 'zzzz-no-such-city'})
            self.assertEqual(cities.status_code, 200)
            self.assertEqual(self._leftovers_of(cities), [], f'{lang} empty cities')
            warehouses = client.get(f'/{lang}/orders/np/warehouses/', {'city_ref': 'no-such-city'})
            self.assertEqual(warehouses.status_code, 200)
            self.assertEqual(self._leftovers_of(warehouses), [], f'{lang} empty warehouses')

    def test_django_builtin_messages_are_not_ukrainian_for_filipino(self):
        from django.utils import translation
        from django.utils.translation import gettext

        with translation.override('fil'):
            self.assertEqual(gettext('This field is required.'), 'Kailangang punan ang field na ito.')

    def test_every_table_phrase_visible_on_cart_and_checkout_is_translated(self):
        paths = []
        client = self._client()
        self._fill_cart(client, 'uk', 1)
        self.client.cookies['age_ok'] = '1'
        self.client.post('/cart/add/', {'product_id': self.product.id, 'quantity': 1})
        paths = ['/cart/', '/orders/checkout/']
        checked = self.assert_phrases_rendered('04-zamovlennia', paths, minimum=30)
        self.assertGreater(checked, 30)
