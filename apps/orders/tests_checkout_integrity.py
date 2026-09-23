from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Brand, Category, Product
from apps.orders.idempotency import checkout_idempotency_key
from apps.orders.models import Order, Payment
from apps.orders.services import nova_poshta as np_svc
from apps.orders.services import payments as pay_svc


class CheckoutIdempotencyTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-ci', is_active=True)
        cat = Category.objects.create(name='Cigars', slug='cigars-ci', kind='cigars', is_active=True)
        self.product = Product.objects.create(
            name='Serie',
            slug='serie-ci',
            brand=brand,
            category=cat,
            base_price=Decimal('500'),
            stock=10,
            is_active=True,
        )

    def _fill_and_token(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        return page.context['checkout_token']

    def _payload(self, token, payment='cod'):
        return {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': payment,
            'age_confirm': '1',
            'checkout_token': token,
        }

    def test_double_submit_same_token_one_order(self):
        token = self._fill_and_token()
        payload = self._payload(token)
        r1 = self.client.post(reverse('orders:checkout'), payload)
        self.assertEqual(r1.status_code, 302)
        # refill cart for second attempt (first cleared it)
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        r2 = self.client.post(reverse('orders:checkout'), payload)
        self.assertEqual(r2.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.idempotency_key, checkout_idempotency_key(token))


@override_settings(DEMO_PAYMENTS=True)
class PaymentWebhookAndReplayTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-pay', is_active=True)
        cat = Category.objects.create(name='Cigars', slug='cigars-pay', kind='cigars', is_active=True)
        self.product = Product.objects.create(
            name='Serie',
            slug='serie-pay',
            brand=brand,
            category=cat,
            base_price=Decimal('500'),
            stock=10,
            is_active=True,
        )

    def _place_online_order(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        resp = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'online',
            'age_confirm': '1',
            'checkout_token': token,
        })
        self.assertEqual(resp.status_code, 302)
        return Order.objects.get()

    def test_webhook_marks_paid_without_redirect(self):
        order = self._place_online_order()
        paid = pay_svc.settle_payment(
            order,
            status='success',
            payload={'status': 'success', 'order_id': order.order_number},
            provider=Payment.PROVIDER_DEMO,
            transaction_id='wh-1',
        )
        self.assertTrue(paid)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_PAID)
        # second webhook must not duplicate
        paid2 = pay_svc.settle_payment(
            order,
            status='success',
            payload={'status': 'success', 'order_id': order.order_number},
            provider=Payment.PROVIDER_DEMO,
            transaction_id='wh-2',
        )
        self.assertFalse(paid2)
        self.assertEqual(Payment.objects.filter(liqpay_order_id=order.order_number).count(), 1)

    def test_pay_page_after_paid_goes_thank_you(self):
        order = self._place_online_order()
        pay_svc.settle_payment(
            order, status='success', payload={'demo': True}, provider=Payment.PROVIDER_DEMO,
        )
        resp = self.client.get(reverse('orders:pay', args=[order.order_number]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(order.order_number, resp.url)

    @override_settings(DEMO_PAYMENTS=False, LIQPAY_PUBLIC_KEY='pub', LIQPAY_PRIVATE_KEY='priv')
    def test_second_pay_visit_waits_no_new_invoice(self):
        order = self._place_online_order()
        # Simulate first LiqPay handoff: pending payment exists
        pay_svc.ensure_pending_payment(order, provider=Payment.PROVIDER_LIQPAY)
        resp = self.client.get(reverse('orders:pay', args=[order.order_number]))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context.get('waiting'))
        self.assertEqual(Payment.objects.filter(liqpay_order_id=order.order_number).count(), 1)


class NovaPoshtaWarehouseValidateTests(TestCase):
    def test_demo_warehouse_ok_and_missing(self):
        self.assertEqual(
            np_svc.warehouse_status('demo-kyiv', 'demo-kyiv-1'),
            'ok',
        )
        self.assertEqual(
            np_svc.warehouse_status('demo-kyiv', 'closed-warehouse'),
            'missing',
        )

    def test_api_error_soft_unverified(self):
        with patch.object(np_svc, 'get_warehouses', side_effect=np_svc.NovaPoshtaError('down')):
            self.assertEqual(
                np_svc.warehouse_status('some-city', 'some-wh'),
                'unverified',
            )

    def test_checkout_rejects_missing_warehouse(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-np', is_active=True)
        cat = Category.objects.create(name='Cigars', slug='cigars-np', kind='cigars', is_active=True)
        product = Product.objects.create(
            name='Serie',
            slug='serie-np',
            brand=brand,
            category=cat,
            base_price=Decimal('500'),
            stock=10,
            is_active=True,
        )
        self.client.post(reverse('cart:add'), {'product_id': product.id, 'quantity': 1})
        page = self.client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        resp = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'nova_poshta',
            'delivery_city': 'Київ',
            'delivery_address': 'Закрите відділення',
            'np_city_ref': 'demo-kyiv',
            'np_warehouse_ref': 'does-not-exist',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': token,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.assertFormError(
            resp.context['form'],
            'delivery_address',
            'Обране відділення більше недоступне. Оберіть інше зі списку.',
        )

    def test_checkout_soft_accepts_unverified_with_marker(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-np2', is_active=True)
        cat = Category.objects.create(name='Cigars', slug='cigars-np2', kind='cigars', is_active=True)
        product = Product.objects.create(
            name='Serie',
            slug='serie-np2',
            brand=brand,
            category=cat,
            base_price=Decimal('500'),
            stock=10,
            is_active=True,
        )
        self.client.post(reverse('cart:add'), {'product_id': product.id, 'quantity': 1})
        page = self.client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        with patch.object(np_svc, 'warehouse_status', return_value='unverified'):
            resp = self.client.post(reverse('orders:checkout'), {
                'first_name': 'Ivan',
                'last_name': 'Petrenko',
                'phone': '+380501112233',
                'email': 'buyer@example.com',
                'delivery_service': 'nova_poshta',
                'delivery_city': 'Київ',
                'delivery_address': 'Відділення №1',
                'np_city_ref': 'demo-kyiv',
                'np_warehouse_ref': 'demo-kyiv-1',
                'payment_method': 'cod',
                'age_confirm': '1',
                'checkout_token': token,
            })
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.get()
        self.assertIn('[RS:NP_UNVERIFIED]', order.comment)
