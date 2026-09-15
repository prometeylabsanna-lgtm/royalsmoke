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
