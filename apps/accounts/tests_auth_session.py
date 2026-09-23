"""Auth session: password change, delete, logout keeps guest cart."""

from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.accounts.sessions import flush_user_sessions
from apps.cart import db_services as db_cart
from apps.cart.services import CART_SESSION_KEY
from apps.catalog.models import Brand, Category, Product

User = get_user_model()


class AuthSessionTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-auth')
        cat = Category.objects.create(name='Cigars', slug='cigars-auth', kind='cigars')
        self.product = Product.objects.create(
            name='Serie Auth',
            slug='serie-auth',
            brand=brand,
            category=cat,
            base_price=900,
            stock=10,
            is_active=True,
        )
        self.user = User.objects.create_user(
            email='owner@example.com',
            password='Secret123!',
        )

    def _other_session(self, user) -> SessionStore:
        other = Client()
        self.assertTrue(other.login(email=user.email, password='Secret123!'))
        other.get(reverse('accounts:cabinet'))
        key = other.session.session_key
        self.assertTrue(Session.objects.filter(session_key=key).exists())
        return other

    def test_password_change_keeps_current_flushes_others(self):
        other = self._other_session(self.user)
        other_key = other.session.session_key

        self.client.login(email=self.user.email, password='Secret123!')
        resp = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'Secret123!',
            'new_password1': 'NewSecret123!',
            'new_password2': 'NewSecret123!',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Session.objects.filter(session_key=other_key).exists())
        # Current session still authenticated
        cab = self.client.get(reverse('accounts:cabinet'))
        self.assertEqual(cab.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecret123!'))

    def test_logout_keeps_cart_as_guest(self):
        self.client.login(email=self.user.email, password='Secret123!')
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
        })
        resp = self.client.post(reverse('accounts:logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(self.client.session.get('_auth_user_id'))
        cart = self.client.session.get(CART_SESSION_KEY) or {}
        self.assertTrue(cart)
        qty = next(iter(cart.values()))['qty']
        self.assertEqual(qty, 2)

    def test_delete_account_clears_sessions_keeps_guest_cart(self):
        other = self._other_session(self.user)
        other_key = other.session.session_key
        db_cart.add_item(self.user, self.product.id, 3)

        self.client.login(email=self.user.email, password='Secret123!')
        uid = self.user.pk
        resp = self.client.post(reverse('accounts:delete_account'), {
            'password': 'Secret123!',
            'confirm': 'on',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(User.objects.filter(pk=uid).exists())
        self.assertFalse(Session.objects.filter(session_key=other_key).exists())
        self.assertFalse(self.client.session.get('_auth_user_id'))
        cart = self.client.session.get(CART_SESSION_KEY) or {}
        self.assertTrue(cart)
        self.assertEqual(next(iter(cart.values()))['qty'], 3)

    def test_flush_user_sessions_helper(self):
        other = self._other_session(self.user)
        other_key = other.session.session_key
        self.client.login(email=self.user.email, password='Secret123!')
        keep = self.client.session.session_key
        n = flush_user_sessions(self.user, keep_session_key=keep)
        self.assertGreaterEqual(n, 1)
        self.assertFalse(Session.objects.filter(session_key=other_key).exists())
        self.assertTrue(Session.objects.filter(session_key=keep).exists())


@override_settings(CHECKOUT_SESSION_SECONDS=120, CHECKOUT_WARN_SECONDS=90)
class CheckoutSlidingSessionTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='Oliva', slug='oliva-slide')
        cat = Category.objects.create(name='Cigars', slug='cigars-slide', kind='cigars')
        self.product = Product.objects.create(
            name='Serie Slide',
            slug='serie-slide',
            brand=brand,
            category=cat,
            base_price=500,
            stock=5,
            is_active=True,
        )

    def test_checkout_touches_expiry_and_warn_flag(self):
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        page = self.client.get(reverse('orders:checkout'))
        self.assertEqual(page.status_code, 200)
        self.assertIsNotNone(self.client.session.get('rs_checkout_expires_at'))
        # With 120s session and 90s warn window, remaining ~120 > 90 → no warn yet
        self.assertFalse(page.context['checkout_show_warn'])
        # Force near-expiry
        session = self.client.session
        session['rs_checkout_expires_at'] = session['rs_checkout_expires_at'] - 100
        session.save()
        # Re-render without touch would warn; but checkout touches again — simulate helper
        from apps.orders.checkout_session import checkout_expiry_context
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware

        rf = RequestFactory()
        req = rf.get('/')
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(req)
        req.session = self.client.session
        ctx = checkout_expiry_context(req)
        self.assertTrue(ctx['checkout_show_warn'])
