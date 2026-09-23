from __future__ import annotations

from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Brand, Category, Product
from apps.orders.models import Order
from apps.pwa.models import PushSubscription
from apps.pwa.services.catalog_snapshot import build_catalog_snapshot
from apps.pwa.services.push import notify_order_push, subscriptions_for_order


User = get_user_model()


class PwaEndpointsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.brand = Brand.objects.create(name='Oliva', slug='oliva', is_active=True)
        self.category = Category.objects.create(name='Cigars', slug='cigars', is_active=True)
        Product.objects.create(
            brand=self.brand,
            category=self.category,
            name='Serie V',
            slug='serie-v',
            base_price=Decimal('100.00'),
            stock=3,
            is_active=True,
        )

    def test_manifest(self):
        resp = self.client.get(reverse('pwa:manifest'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/manifest+json', resp['Content-Type'])
        data = resp.json()
        self.assertEqual(data['display'], 'standalone')
        self.assertTrue(data['icons'])

    def test_service_worker(self):
        resp = self.client.get(reverse('pwa:sw'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('javascript', resp['Content-Type'])
        self.assertEqual(resp['Service-Worker-Allowed'], '/')
        self.assertIn('rs-pwa-shell-v1', resp.content.decode())

    def test_offline_catalog_json(self):
        resp = self.client.get(reverse('pwa:offline_catalog'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('uk', data['langs'])
        self.assertIn('en', data['langs'])
        self.assertIn('zh-hans', data['langs'])
        self.assertEqual(len(data['langs']['uk']['products']), 1)
        self.assertEqual(data['langs']['uk']['products'][0]['slug'], 'serie-v')

    def test_snapshot_builder(self):
        snap = build_catalog_snapshot()
        self.assertEqual(snap['version'], 1)
        self.assertTrue(snap['langs']['uk']['categories'])
        self.assertTrue(snap['langs']['uk']['brands'])


@override_settings(VAPID_PUBLIC_KEY='test-public', VAPID_PRIVATE_KEY='test-private')
class PwaPushTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='buyer@example.com', password='Passw0rd!')
        self.order = Order.objects.create(
            user=self.user,
            first_name='A',
            last_name='B',
            phone='+380501112233',
            email='buyer@example.com',
            delivery_service=Order.DELIVERY_PICKUP,
            delivery_city='Kyiv',
            delivery_address='Shop',
            payment_method=Order.PAYMENT_ONLINE,
            subtotal=Decimal('100.00'),
            total=Decimal('100.00'),
            status=Order.STATUS_PROCESSING,
        )
        self.sub = PushSubscription.objects.create(
            endpoint='https://push.example/endpoint-1',
            p256dh='x' * 40,
            auth='y' * 20,
            user=self.user,
            email='buyer@example.com',
            language='en',
        )

    def test_subscribe_creates_row(self):
        resp = self.client.post(
            reverse('pwa:push_subscribe'),
            data='{"endpoint":"https://push.example/e2","keys":{"p256dh":"abc","auth":"def"},"language":"uk"}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            PushSubscription.objects.filter(endpoint='https://push.example/e2', is_active=True).exists()
        )

    def test_bind_email(self):
        resp = self.client.post(
            reverse('pwa:push_bind'),
            data='{"endpoint":"https://push.example/endpoint-1","email":"guest@example.com"}',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.email, 'guest@example.com')

    def test_subscriptions_for_order(self):
        qs = subscriptions_for_order(self.order)
        self.assertEqual(qs.count(), 1)

    @patch('apps.pwa.services.push.send_web_push', return_value=True)
    def test_status_push_language(self, mock_send):
        sent = notify_order_push(self.order, kind='status')
        self.assertEqual(sent, 1)
        mock_send.assert_called_once()
        payload = mock_send.call_args[0][1]
        self.assertIn('title', payload)
        self.assertEqual(payload['tag'], f'order-status-{self.order.order_number}-processing')

    @patch('apps.pwa.services.push.notify_order_push')
    def test_status_change_triggers_push(self, mock_notify):
        with self.captureOnCommitCallbacks(execute=True):
            self.order.status = Order.STATUS_SHIPPED
            self.order.save(update_fields=['status', 'updated_at'])
        mock_notify.assert_called()
        self.assertEqual(mock_notify.call_args.kwargs.get('kind'), 'status')
