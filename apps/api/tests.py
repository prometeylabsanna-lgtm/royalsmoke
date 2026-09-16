from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.catalog.models import Brand, Category, Product

User = get_user_model()


class ApiAuthCartTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.brand = Brand.objects.create(name='B', slug='b')
        self.cat = Category.objects.create(name='C', slug='c', kind='cigars')
        self.product = Product.objects.create(
            name='P',
            slug='p',
            brand=self.brand,
            category=self.cat,
            base_price=100,
            is_active=True,
        )

    def test_register_login_cart_checkout_cod(self):
        r = self.client.post('/api/v1/auth/register/', {
            'email': 'a@example.com',
            'password': 'Secret123!',
            'first_name': 'A',
            'last_name': 'B',
        }, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        token = r.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        r = self.client.post('/api/v1/cart/', {
            'product_id': self.product.id,
            'quantity': 2,
        }, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['count'], 2)
        r = self.client.post('/api/v1/checkout/', {
            'first_name': 'A',
            'last_name': 'B',
            'phone': '+380501112233',
            'email': 'a@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': True,
        }, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        self.assertEqual(r.json()['status'], 'pending')

    @override_settings(DEMO_PAYMENTS=True)
    def test_checkout_online_demo_url(self):
        r = self.client.post('/api/v1/auth/register/', {
            'email': 'pay@example.com',
            'password': 'Secret123!',
            'first_name': 'A',
            'last_name': 'B',
        }, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {r.json()["token"]}')
        self.client.post('/api/v1/cart/', {
            'product_id': self.product.id,
            'quantity': 1,
        }, format='json')
        r = self.client.post('/api/v1/checkout/', {
            'first_name': 'A',
            'last_name': 'B',
            'phone': '+380501112233',
            'email': 'pay@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'online',
            'age_confirm': True,
        }, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        body = r.json()
        self.assertEqual(body['status'], 'awaiting_payment')
        self.assertTrue(body.get('demo'))
        self.assertIn('/orders/pay/', body.get('demo_pay_url') or '')
