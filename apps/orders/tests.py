import base64
import json
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from apps.orders.services import liqpay as liqpay_svc


@override_settings(LIQPAY_PUBLIC_KEY='pub', LIQPAY_PRIVATE_KEY='priv', LIQPAY_SANDBOX=True)
class LiqPayServiceTests(SimpleTestCase):
    def test_sign_roundtrip(self):
        class O:
            order_number = 'RTEST001'
            total = 100
            currency = 'UAH'

        payload = liqpay_svc.create_checkout_payload(
            O(),
            result_url='https://example.com/r',
            server_url='https://example.com/c',
        )
        decoded = liqpay_svc.verify_callback(payload['data'], payload['signature'])
        self.assertEqual(decoded['order_id'], 'RTEST001')
        self.assertEqual(decoded['amount'], 100.0)

    def test_bad_signature(self):
        data = base64.b64encode(json.dumps({'order_id': 'x'}).encode()).decode()
        with self.assertRaises(ValueError):
            liqpay_svc.verify_callback(data, 'bad')


class HealthTests(TestCase):
    def test_health(self):
        resp = self.client.get(reverse('health'))
        self.assertIn(resp.status_code, (200, 503))
        self.assertIn('db', resp.json())

    def test_healthz(self):
        resp = self.client.get(reverse('healthz'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b'ok')


class CheckoutAndDemoPayTests(TestCase):
    def setUp(self):
        from apps.catalog.models import Brand, Category, Product

        brand = Brand.objects.create(name='Oliva', slug='oliva')
        cat = Category.objects.create(name='Cigars', slug='cigars', kind='cigars')
        self.product = Product.objects.create(
            name='Serie V',
            slug='serie-v',
            brand=brand,
            category=cat,
            base_price=1200,
            is_active=True,
        )

    def _fill_cart(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })

    def _checkout(self, payment_method='online'):
        return self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': payment_method,
            'age_confirm': '1',
        })

    def test_cod_checkout(self):
        self._fill_cart()
        resp = self._checkout('cod')
        self.assertEqual(resp.status_code, 302)
        from apps.orders.models import Order
        order = Order.objects.get()
        self.assertEqual(order.status, Order.STATUS_PENDING)
        self.assertEqual(order.payment_method, Order.PAYMENT_COD)
        self.assertEqual(resp.url, order.get_absolute_url())

    @override_settings(DEMO_PAYMENTS=True)
    def test_demo_pay_success_and_failure(self):
        from apps.orders.models import Order, Payment

        self._fill_cart()
        resp = self._checkout('online')
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.status, Order.STATUS_AWAITING_PAYMENT)
        self.assertIn(f'/orders/pay/{order.order_number}/', resp.url)

        pay_page = self.client.get(reverse('orders:pay', args=[order.order_number]))
        self.assertEqual(pay_page.status_code, 200)
        self.assertContains(pay_page, 'Демо-режим')

        fail = self.client.post(
            reverse('orders:demo_pay', args=[order.order_number]),
            {'outcome': 'failure'},
        )
        self.assertEqual(fail.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_AWAITING_PAYMENT)
        self.assertEqual(Payment.objects.get().status, Payment.STATUS_FAILURE)

        ok = self.client.post(
            reverse('orders:demo_pay', args=[order.order_number]),
            {'outcome': 'success'},
        )
        self.assertEqual(ok.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_PAID)
        self.assertEqual(Payment.objects.get().status, Payment.STATUS_SUCCESS)

        thank = self.client.get(order.get_absolute_url())
        self.assertContains(thank, order.order_number)

    @override_settings(DEMO_PAYMENTS=False)
    def test_demo_pay_disabled(self):
        self._fill_cart()
        self._checkout('online')
        from apps.orders.models import Order
        order = Order.objects.get()
        resp = self.client.post(
            reverse('orders:demo_pay', args=[order.order_number]),
            {'outcome': 'success'},
        )
        self.assertEqual(resp.status_code, 403)
        order.refresh_from_db()
        self.assertNotEqual(order.status, Order.STATUS_PAID)
