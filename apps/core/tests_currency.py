from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from apps.catalog.models import Brand, Category, Product
from apps.core.currency import (
    clear_currency_cache,
    convert_from_uah,
    language_currency_code,
)
from apps.core.models import CurrencyRate
from apps.orders.models import Order


class CurrencyServiceTests(TestCase):
    def setUp(self):
        usd = CurrencyRate.objects.get(code='USD')
        usd.uah_per_unit = Decimal('40.0000')
        usd.save()
        cny = CurrencyRate.objects.get(code='CNY')
        cny.uah_per_unit = Decimal('5.0000')
        cny.save()
        clear_currency_cache()

    def test_language_mapping(self):
        self.assertEqual(language_currency_code('uk'), 'UAH')
        self.assertEqual(language_currency_code('en'), 'USD')
        self.assertEqual(language_currency_code('zh-hans'), 'CNY')

    def test_convert_from_uah(self):
        self.assertEqual(convert_from_uah(Decimal('1200'), 'UAH'), Decimal('1200.00'))
        self.assertEqual(convert_from_uah(Decimal('1200'), 'USD'), Decimal('30.00'))
        self.assertEqual(convert_from_uah(Decimal('1200'), 'CNY'), Decimal('240.00'))


class StorefrontCurrencyTests(TestCase):
    def setUp(self):
        usd = CurrencyRate.objects.get(code='USD')
        usd.uah_per_unit = Decimal('40.0000')
        usd.save()
        clear_currency_cache()
        brand = Brand.objects.create(name='Oliva', slug='oliva')
        cat = Category.objects.create(name='Cigars', slug='cigars', kind='cigars')
        self.product = Product.objects.create(
            name='Serie V',
            slug='serie-v',
            brand=brand,
            category=cat,
            base_price=Decimal('1200'),
            is_active=True,
        )

    def test_uk_shows_uah(self):
        with translation.override('uk'):
            url = reverse('catalog:list')
        resp = self.client.get(url)
        self.assertContains(resp, '₴')
        self.assertContains(resp, '1200')

    def test_en_shows_usd(self):
        with translation.override('en'):
            url = reverse('catalog:list')
        resp = self.client.get(url)
        self.assertContains(resp, '$')
        self.assertContains(resp, '30.00')
        self.assertNotContains(resp, '₴')

    def test_en_checkout_stores_usd(self):
        with translation.override('en'):
            add_url = reverse('cart:add')
            checkout_url = reverse('orders:checkout')
        self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 1,
        })
        resp = self.client.post(checkout_url, {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
        })
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.currency, 'USD')
        self.assertEqual(order.total, Decimal('30.00'))
        self.assertEqual(order.fx_rate, Decimal('40.0000'))
        self.assertEqual(order.items.get().price, Decimal('30.00'))


@override_settings(LANGUAGE_CURRENCY={'uk': 'UAH', 'en': 'USD', 'zh-hans': 'CNY', 'de': 'EUR'})
class FutureLanguageMappingTests(TestCase):
    def test_unknown_language_falls_back_to_uah_rate_table(self):
        with translation.override('de'):
            self.assertEqual(language_currency_code(), 'EUR')
