from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Brand, Category, Product


class CartFlowTests(TestCase):
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

    def test_add_update_remove(self):
        add_url = reverse('cart:add')
        resp = self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.assertEqual(resp.status_code, 302)
        session = self.client.session
        self.assertTrue(any(v.get('product_id') == self.product.id for v in session.get('rs_cart', {}).values()))

        resp = self.client.post(reverse('cart:update'), {
            'product_id': self.product.id,
            'quantity': 3,
        })
        self.assertEqual(resp.status_code, 302)
        qty = next(v['qty'] for v in self.client.session['rs_cart'].values())
        self.assertEqual(qty, 3)

        resp = self.client.post(
            add_url,
            {'product_id': self.product.id, 'quantity': 1},
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="cart-badge"')
        self.assertContains(resp, '4')

        resp = self.client.post(reverse('cart:remove'), {'product_id': self.product.id})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.client.session.get('rs_cart'), {})

    def test_invalid_product_does_not_500(self):
        resp = self.client.post(reverse('cart:add'), {'product_id': 'abc'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post(reverse('cart:add'), {'product_id': 999999})
        self.assertEqual(resp.status_code, 302)
