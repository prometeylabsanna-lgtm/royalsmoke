from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.catalog.admin import ProductAdminForm
from apps.catalog.models import Brand, Category, Product
from apps.core.money import (
    MIN_UNIT_PRICE,
    apply_sale_percents,
    line_total,
    money,
    reconcile_order_totals,
    sum_money,
)
from apps.orders.models import Order, OrderItem


class MoneyRoundingTests(TestCase):
    def test_three_times_33_33_is_99_99(self):
        unit = money('33.33')
        self.assertEqual(line_total(unit, 3), money('99.99'))
        self.assertEqual(sum_money([unit, unit, unit]), money('99.99'))

    def test_half_up_rounding(self):
        self.assertEqual(money('1.005'), money('1.01'))
        self.assertEqual(money('1.004'), money('1.00'))


class SaleStackingTests(TestCase):
    def test_stacked_sales_never_free_or_negative(self):
        price = apply_sale_percents(Decimal('1000'), [50, 50, 50])
        self.assertEqual(price, money('125.00'))
        self.assertGreaterEqual(price, MIN_UNIT_PRICE)
        price = apply_sale_percents(Decimal('1000'), [100, 50])
        self.assertEqual(price, MIN_UNIT_PRICE)
        price = apply_sale_percents(Decimal('1000'), [20, 30])
        self.assertEqual(price, money('560.00'))
        with self.assertRaises(ValueError):
            apply_sale_percents(Decimal('0'), [10])


class ZeroPriceGuardsTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='B', slug='b', is_active=True)
        self.cat = Category.objects.create(name='C', slug='c', kind='cigars', is_active=True)
        self.free = Product.objects.create(
            name='Free',
            slug='free',
            brand=self.brand,
            category=self.cat,
            base_price=Decimal('0'),
            stock=5,
            is_active=True,
        )
        self.paid = Product.objects.create(
            name='Paid',
            slug='paid',
            brand=self.brand,
            category=self.cat,
            base_price=Decimal('33.33'),
            stock=5,
            is_active=True,
        )

    def test_cannot_add_zero_price_to_cart(self):
        resp = self.client.post(reverse('cart:add'), {
            'product_id': self.free.id,
            'quantity': 1,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.client.session.get('rs_cart'), {})

    def test_zero_price_in_session_blocks_checkout(self):
        session = self.client.session
        session['rs_cart'] = {str(self.free.id): {'product_id': self.free.id, 'qty': 1}}
        session.save()
        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['can_checkout'])
        self.assertTrue(resp.context['cart_issues'])

    def test_admin_form_rejects_zero_price(self):
        form = ProductAdminForm(data={
            'brand': self.brand.id,
            'category': self.cat.id,
            'name': 'X',
            'slug': 'x-zero',
            'base_price': '0',
            'stock': 1,
            'is_active': True,
            'sort_order': 0,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('base_price', form.errors)

    def test_model_clean_rejects_zero(self):
        p = Product(
            brand=self.brand,
            category=self.cat,
            name='Y',
            slug='y-zero',
            base_price=Decimal('0'),
        )
        with self.assertRaises(ValidationError):
            p.full_clean()


class OrderReconcileTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name='B2', slug='b2', is_active=True)
        cat = Category.objects.create(name='C2', slug='c2', kind='cigars', is_active=True)
        self.product = Product.objects.create(
            name='P',
            slug='p-rec',
            brand=brand,
            category=cat,
            base_price=Decimal('33.33'),
            stock=10,
            is_active=True,
        )

    def test_reconcile_ok_for_consistent_order(self):
        order = Order.objects.create(
            first_name='A',
            last_name='B',
            phone='+380501112233',
            email='a@example.com',
            delivery_service='pickup',
            delivery_city='Kyiv',
            delivery_address='Showroom',
            payment_method='cod',
            subtotal=money('99.99'),
            discount=money('0'),
            delivery_cost=money('0'),
            total=money('99.99'),
            currency='UAH',
            fx_rate=money('1'),
            status=Order.STATUS_PENDING,
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name='P',
            product_sku='',
            price=money('33.33'),
            quantity=3,
            line_total=money('99.99'),
        )
        self.assertEqual(reconcile_order_totals(order), money('99.99'))

    def test_reconcile_detects_mismatch(self):
        order = Order.objects.create(
            first_name='A',
            last_name='B',
            phone='+380501112233',
            email='a@example.com',
            delivery_service='pickup',
            delivery_city='Kyiv',
            delivery_address='Showroom',
            payment_method='online',
            subtotal=money('99.99'),
            discount=money('0'),
            delivery_cost=money('0'),
            total=money('99.98'),
            currency='UAH',
            fx_rate=money('1'),
            status=Order.STATUS_AWAITING_PAYMENT,
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name='P',
            product_sku='',
            price=money('33.33'),
            quantity=3,
            line_total=money('99.99'),
        )
        with self.assertRaises(ValueError):
            reconcile_order_totals(order)
