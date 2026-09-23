"""Order access / IDOR for thank-you and pay."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Brand, Category, Product
from apps.orders.models import Order

User = get_user_model()


@override_settings(DEMO_PAYMENTS=True)
class OrderAccessTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-idor')
        cat = Category.objects.create(name='Cigars', slug='cigars-idor', kind='cigars')
        self.product = Product.objects.create(
            name='Serie IDOR',
            slug='serie-idor',
            brand=brand,
            category=cat,
            base_price=800,
            stock=20,
            is_active=True,
        )
        self.owner = User.objects.create_user(
            email='owner-idor@example.com',
            password='Secret123!',
        )
        self.other = User.objects.create_user(
            email='other-idor@example.com',
            password='Secret123!',
        )

    def _checkout_as(self, client, *, payment_method='cod', login_user=None):
        if login_user:
            client.login(email=login_user.email, password='Secret123!')
        client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        return client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': payment_method,
            'age_confirm': '1',
            'checkout_token': token,
        })

    def test_guest_order_thank_you_by_number(self):
        resp = self._checkout_as(self.client)
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.latest('id')
        self.assertIsNone(order.user_id)
        # Fresh client without session still can open guest thank-you by number
        stranger = Client()
        thanks = stranger.get(reverse('orders:thank_you', args=[order.order_number]))
        self.assertEqual(thanks.status_code, 200)

    def test_auth_order_blocked_for_stranger(self):
        resp = self._checkout_as(self.client, login_user=self.owner)
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.latest('id')
        self.assertEqual(order.user_id, self.owner.id)

        # Owner can view
        thanks = self.client.get(reverse('orders:thank_you', args=[order.order_number]))
        self.assertEqual(thanks.status_code, 200)

        # Other authenticated user cannot
        other_c = Client()
        other_c.login(email=self.other.email, password='Secret123!')
        denied = other_c.get(reverse('orders:thank_you', args=[order.order_number]))
        self.assertEqual(denied.status_code, 403)

        # Anonymous stranger cannot
        anon = Client()
        denied2 = anon.get(reverse('orders:thank_you', args=[order.order_number]))
        self.assertEqual(denied2.status_code, 403)

    def test_auth_order_pay_blocked_for_stranger(self):
        resp = self._checkout_as(self.client, payment_method='online', login_user=self.owner)
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.latest('id')
        self.assertEqual(order.payment_method, Order.PAYMENT_ONLINE)

        other_c = Client()
        other_c.login(email=self.other.email, password='Secret123!')
        denied = other_c.get(reverse('orders:pay', args=[order.order_number]))
        self.assertEqual(denied.status_code, 403)

        ok = self.client.get(reverse('orders:pay', args=[order.order_number]))
        self.assertEqual(ok.status_code, 200)

    def test_cabinet_lists_only_own_orders(self):
        self._checkout_as(self.client, login_user=self.owner)
        own = Order.objects.filter(user=self.owner).latest('id')

        other_c = Client()
        self._checkout_as(other_c, login_user=self.other)
        other_order = Order.objects.filter(user=self.other).latest('id')

        cab = self.client.get(reverse('accounts:cabinet'))
        self.assertEqual(cab.status_code, 200)
        nums = [o.order_number for o in cab.context['orders']]
        self.assertIn(own.order_number, nums)
        self.assertNotIn(other_order.order_number, nums)
