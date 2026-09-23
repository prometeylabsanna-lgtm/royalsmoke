from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.cart import db_services as db_cart
from apps.cart import services as session_cart
from apps.cart import stock as stock_svc
from apps.cart.models import CartItem, CartReservation
from apps.catalog.models import Brand, Category, Product

User = get_user_model()


class CartFixturesMixin:
    def _make_product(self, *, slug='serie-v', price='1200', stock=10):
        brand, _ = Brand.objects.get_or_create(name='Oliva', defaults={'slug': 'oliva'})
        cat, _ = Category.objects.get_or_create(
            slug='cigars', defaults={'name': 'Cigars', 'kind': 'cigars'},
        )
        return Product.objects.create(
            name=f'Product {slug}',
            slug=slug,
            brand=brand,
            category=cat,
            base_price=Decimal(price),
            stock=stock,
            is_active=True,
        )


class CartFlowTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product()

    def test_add_update_remove(self):
        add_url = reverse('cart:add')
        resp = self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.assertEqual(resp.status_code, 302)
        session = self.client.session
        self.assertTrue(any(v.get('product_id') == self.product.id for v in session.get('rs_cart', {}).values()))
        self.assertEqual(CartReservation.objects.filter(product=self.product).count(), 1)

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
        self.assertEqual(CartReservation.objects.filter(product=self.product).count(), 0)

    def test_invalid_product_does_not_500(self):
        resp = self.client.post(reverse('cart:add'), {'product_id': 'abc'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post(reverse('cart:add'), {'product_id': 999999})
        self.assertEqual(resp.status_code, 302)


class CartPriceAvailabilityTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(stock=5, price='1000')

    def test_checkout_uses_live_price_silently(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
        })
        self.product.base_price = Decimal('1500')
        self.product.save(update_fields=['base_price'])

        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 200)
        cart = resp.context['cart']
        self.assertEqual(cart['total'], Decimal('3000'))
        self.assertEqual(cart['issues'], [])
        self.assertTrue(cart['can_checkout'])

    def test_checkout_blocked_when_out_of_stock(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
        })
        Product.objects.filter(pk=self.product.id).update(stock=0)

        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['can_checkout'])
        self.assertTrue(resp.context['cart_issues'])

        post = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': resp.context['checkout_token'],
        })
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post.url, reverse('orders:checkout'))
        from apps.orders.models import Order
        self.assertEqual(Order.objects.count(), 0)

    def test_qty_capped_by_stock_on_add(self):
        self.product.stock = 2
        self.product.save(update_fields=['stock'])
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 9,
        })
        qty = next(v['qty'] for v in self.client.session['rs_cart'].values())
        self.assertEqual(qty, 2)


class CartMergeTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(stock=10)
        self.user = User.objects.create_user(
            email='buyer@example.com',
            password='Secret123!',
        )

    def test_merge_takes_max_and_caps_stock(self):
        session = SessionStore()
        session.create()
        session_cart.add_item(session, self.product.id, 5)
        session.save()

        cart = db_cart.get_or_create_cart(self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        stock_svc.set_reservation(self.product.id, 2, user=self.user)

        db_cart.merge_session_into_user(session, self.user)
        item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(item.quantity, 5)

        # Over stock: guest 8 + user 9 → max 9 but stock 10 OK; with stock 6 → 6
        self.product.stock = 6
        self.product.save(update_fields=['stock'])
        CartReservation.objects.all().delete()
        CartItem.objects.filter(cart__user=self.user).update(quantity=4)
        stock_svc.set_reservation(self.product.id, 4, user=self.user)

        session2 = SessionStore()
        session2.create()
        # Direct raw to avoid session reservation fighting allocatable during setup
        session2['rs_cart'] = {str(self.product.id): {'product_id': self.product.id, 'qty': 6}}
        session2.save()
        stock_svc.set_reservation(self.product.id, 6, session_key=session2.session_key)

        db_cart.merge_session_into_user(session2, self.user)
        item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(item.quantity, 6)

    def test_web_login_merges_guest_cart(self):
        db_cart.add_item(self.user, self.product.id, 2)
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 5,
        })
        resp = self.client.post(reverse('accounts:login'), {
            'username': 'buyer@example.com',
            'password': 'Secret123!',
        })
        self.assertEqual(resp.status_code, 302)
        item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(item.quantity, 5)


class CartCurrencyDisplayTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(price='1000', stock=5)

    def test_totals_stay_uah_base_converted_on_display(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        totals = session_cart.cart_totals(self.client.session)
        self.assertEqual(totals['total'], Decimal('1000'))


@override_settings(SESSION_COOKIE_AGE=60 * 60 * 24 * 30, SESSION_EXPIRE_AT_BROWSER_CLOSE=True)
class CartSessionAndReservationTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(stock=3)

    def test_settings_ttl_and_browser_close(self):
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, 60 * 60 * 24 * 30)
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

    def test_add_reserves_stock_for_others(self):
        c1 = Client()
        c2 = Client()
        c1.post(reverse('cart:add'), {'product_id': self.product.id, 'quantity': 2})
        c2.post(reverse('cart:add'), {'product_id': self.product.id, 'quantity': 5})
        qty2 = next(v['qty'] for v in c2.session['rs_cart'].values())
        self.assertEqual(qty2, 1)
        self.assertEqual(self.product.available_stock(), 0)

    def test_checkout_consumes_stock_and_releases_reservation(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
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
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': token,
        })
        self.assertEqual(resp.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(CartReservation.objects.count(), 0)


class CartConcurrencyAndValidationTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(stock=50, price='100')

    def test_multi_tab_last_write_wins(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 5,
        })
        self.client.post(reverse('cart:update'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.client.post(reverse('cart:remove'), {
            'product_id': self.product.id,
        })
        self.assertEqual(self.client.session.get('rs_cart'), {})

    def test_htmx_update_returns_oob_badge(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
        })
        resp = self.client.post(
            reverse('cart:update'),
            {'product_id': self.product.id, 'quantity': 3},
            HTTP_HX_REQUEST='true',
            HTTP_HX_TARGET='cart-body',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="cart-badge"')
        self.assertContains(resp, 'hx-swap-oob')
        self.assertContains(resp, 'rs-cart-line')

    def test_invalid_qty_never_500(self):
        for raw in ('abc', '1.5', '-5', '999999'):
            resp = self.client.post(reverse('cart:add'), {
                'product_id': self.product.id,
                'quantity': raw,
            })
            self.assertEqual(resp.status_code, 302, raw)
        qty = next(v['qty'] for v in self.client.session['rs_cart'].values())
        self.assertLessEqual(qty, 99)
        self.assertGreaterEqual(qty, 1)

        resp = self.client.post(reverse('cart:update'), {
            'product_id': self.product.id,
            'quantity': 'abc',
        })
        self.assertEqual(resp.status_code, 302)
        qty = next(v['qty'] for v in self.client.session['rs_cart'].values())
        self.assertEqual(qty, 1)

        resp = self.client.post(reverse('cart:update'), {
            'product_id': self.product.id,
            'quantity': '-3',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.client.session.get('rs_cart'), {})

    def test_hard_limit_99(self):
        self.product.stock = 500
        self.product.save(update_fields=['stock'])
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 200,
        })
        qty = next(v['qty'] for v in self.client.session['rs_cart'].values())
        self.assertEqual(qty, 99)

    def test_inactive_product_keeps_row_blocks_checkout(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.product.is_active = False
        self.product.save(update_fields=['is_active'])
        totals = session_cart.cart_totals(self.client.session)
        self.assertEqual(len(totals['items']), 1)
        self.assertFalse(totals['can_checkout'])
        self.assertTrue(totals['issues'])
        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['can_checkout'])

    def test_deleted_product_keeps_stub_no_500(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        pid = self.product.id
        self.product.delete()
        totals = session_cart.cart_totals(self.client.session)
        self.assertEqual(len(totals['items']), 1)
        self.assertTrue(totals['items'][0]['is_missing'])
        self.assertFalse(totals['can_checkout'])
        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['can_checkout'])
        cart_page = self.client.get(reverse('cart:detail'))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, 'недоступний')
        # update on missing silently keeps row
        self.client.post(reverse('cart:update'), {'product_id': pid, 'quantity': 2})
        self.assertIn(str(pid), self.client.session['rs_cart'])

    def test_live_price_name_change_ok(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
        })
        self.product.name = 'Renamed'
        self.product.base_price = Decimal('250')
        self.product.save(update_fields=['name', 'base_price'])
        totals = session_cart.cart_totals(self.client.session)
        self.assertEqual(totals['total'], Decimal('500'))
        self.assertEqual(totals['items'][0]['product'].name, 'Renamed')
        self.assertTrue(totals['can_checkout'])


class CartDuplicateCheckoutTests(CartFixturesMixin, TestCase):
    def setUp(self):
        self.product = self._make_product(stock=10)

    def _place_order(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        return self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': token,
        })

    def test_back_to_cart_shows_empty_and_flash(self):
        resp = self._place_order()
        self.assertEqual(resp.status_code, 302)
        from apps.orders.models import Order
        order = Order.objects.get()
        cart = self.client.get(reverse('cart:detail'))
        self.assertEqual(cart.status_code, 200)
        self.assertEqual(cart.context['cart']['count'], 0)
        msgs = [str(m) for m in cart.context['messages']]
        self.assertTrue(any('вже створено' in m for m in msgs))

        replay = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': 'stale-token',
        })
        self.assertEqual(replay.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertIn(order.order_number, replay.url)

    def test_reuse_checkout_token_blocked(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        token = page.context['checkout_token']
        payload = {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': token,
        }
        self.assertEqual(self.client.post(reverse('orders:checkout'), payload).status_code, 302)
        # refill cart and replay same token
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        replay = self.client.post(reverse('orders:checkout'), payload)
        self.assertEqual(replay.status_code, 302)
        from apps.orders.models import Order
        self.assertEqual(Order.objects.count(), 1)

    def test_checkout_thank_you_no_store(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        self.assertIn('no-store', page.headers.get('Cache-Control', ''))
        token = page.context['checkout_token']
        self.client.post(reverse('orders:checkout'), {
            'first_name': 'Ivan',
            'last_name': 'Petrenko',
            'phone': '+380501112233',
            'email': 'buyer@example.com',
            'delivery_service': 'pickup',
            'delivery_city': 'Kyiv',
            'delivery_address': 'Showroom',
            'payment_method': 'cod',
            'age_confirm': '1',
            'checkout_token': token,
        })
        from apps.orders.models import Order
        order = Order.objects.get()
        thanks = self.client.get(reverse('orders:thank_you', args=[order.order_number]))
        self.assertIn('no-store', thanks.headers.get('Cache-Control', ''))
