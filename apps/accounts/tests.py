from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import WishlistItem
from apps.catalog.models import Brand, Category, Product

User = get_user_model()


class WishlistAndAuthTests(TestCase):
    def setUp(self):
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

    def test_guest_toggle_session(self):
        url = reverse('accounts:wishlist_toggle')
        resp = self.client.post(url, {'product_id': self.product.id})
        self.assertEqual(resp.status_code, 302)
        self.assertIn(self.product.id, self.client.session.get('rs_wishlist', []))
        self.client.post(url, {'product_id': self.product.id})
        self.assertNotIn(self.product.id, self.client.session.get('rs_wishlist', []))

    def test_register_merges_wishlist(self):
        self.client.post(reverse('accounts:wishlist_toggle'), {'product_id': self.product.id})
        resp = self.client.post(reverse('accounts:register'), {
            'email': 'guest@example.com',
            'password1': 'Secret123!',
            'password2': 'Secret123!',
            'age_confirm': 'on',
        })
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(email='guest@example.com')
        self.assertTrue(WishlistItem.objects.filter(user=user, product=self.product).exists())

    def test_login_keeps_next(self):
        user = User.objects.create_user(email='a@example.com', password='Secret123!')
        resp = self.client.post(reverse('accounts:login'), {
            'username': 'a@example.com',
            'password': 'Secret123!',
            'next': '/cart/',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/cart/')
        self.assertEqual(user.email, 'a@example.com')
