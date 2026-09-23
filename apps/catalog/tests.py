from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.catalog.models import Brand, Category, Product
from apps.catalog.pagination import CATALOG_PAGE_SIZE, paginate_catalog
from apps.catalog.search import (
    SEARCH_MAX_LEN,
    cyr_to_lat,
    lat_to_cyr,
    product_search_q,
    sanitize_search_query,
    search_variants,
)


class CatalogSearchHelpersTests(TestCase):
    def test_sanitize_strips_null_and_limits_length(self):
        raw = 'a' * (SEARCH_MAX_LEN + 50)
        cleaned = sanitize_search_query('\x00' + raw + '\x00')
        self.assertEqual(len(cleaned), SEARCH_MAX_LEN)
        self.assertNotIn('\x00', cleaned)

    def test_translit_round_variants(self):
        self.assertIn('oliva', [v.casefold() for v in search_variants('Оліва')])
        self.assertTrue(any('ол' in v.casefold() for v in search_variants('ol')))
        self.assertEqual(cyr_to_lat('Привіт')[0].lower(), 'p')
        self.assertTrue(lat_to_cyr('oliva'))


class CatalogSearchViewTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Oliva', slug='oliva', is_active=True)
        self.cat = Category.objects.create(name='Cigars', slug='cigars', kind='cigars', is_active=True)
        self.product = Product.objects.create(
            name='Serie V Melanio',
            slug='serie-v-melanio',
            brand=self.brand,
            category=self.cat,
            base_price=Decimal('1200'),
            stock=5,
            is_active=True,
        )

    def test_special_queries_never_500(self):
        payloads = [
            "' OR 1=1 --",
            '<script>alert(1)</script>',
            '🔥',
            '%',
            '&',
            'NULL',
            '_' * 10,
            'a' * 500,
        ]
        for q in payloads:
            resp = self.client.get(reverse('catalog:search'), {'q': q})
            self.assertEqual(resp.status_code, 200, q)
            self.assertNotContains(resp, '<script>alert(1)</script>')
            # Catalog list with same q must also survive
            list_resp = self.client.get(reverse('catalog:list'), {'q': q})
            self.assertEqual(list_resp.status_code, 200, q)

    def test_percent_underscore_not_wildcards(self):
        Product.objects.create(
            name='100% Habano',
            slug='habano-100',
            brand=self.brand,
            category=self.cat,
            base_price=Decimal('900'),
            stock=3,
            is_active=True,
        )
        total = Product.objects.on_storefront().count()
        self.assertGreaterEqual(total, 2)
        # Literal "%" must not act as LIKE wildcard (would match all rows).
        matched = Product.objects.on_storefront().filter(product_search_q('%'))
        self.assertEqual(matched.count(), 1)
        matched = Product.objects.on_storefront().filter(product_search_q('100%'))
        self.assertEqual(matched.count(), 1)
        matched = Product.objects.on_storefront().filter(product_search_q('_'))
        self.assertEqual(matched.count(), 0)

    def test_case_insensitive_and_translit_brand(self):
        qs = Product.objects.on_storefront().filter(product_search_q('oliva'))
        self.assertEqual(qs.count(), 1)
        qs = Product.objects.on_storefront().filter(product_search_q('ОЛІВА'))
        self.assertEqual(qs.count(), 1)
        qs = Product.objects.on_storefront().filter(product_search_q('serie'))
        self.assertEqual(qs.count(), 1)

    def test_suggest_min_length(self):
        resp = self.client.get(reverse('catalog:search'), {'q': 'o'})
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'Serie V')


@override_settings(LANGUAGE_CODE='uk')
class CatalogPaginationTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Padron', slug='padron', is_active=True)
        self.cat = Category.objects.create(name='Cigars', slug='cigars', kind='cigars', is_active=True)
        self.products = []
        for i in range(CATALOG_PAGE_SIZE + 5):
            self.products.append(Product.objects.create(
                name=f'Stick {i:03d}',
                slug=f'stick-{i:03d}',
                brand=self.brand,
                category=self.cat,
                base_price=Decimal('100') + i,
                stock=2,
                is_active=True,
                sort_order=i,
            ))

    def test_page_out_of_range_empty_not_404(self):
        resp = self.client.get(reverse('catalog:list'), {
            'page': 99,
            'brand': 'padron',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['products']), 0)
        self.assertContains(resp, 'Нічого не знайдено')
        self.assertTrue(getattr(resp.context['page_obj'], 'out_of_range', False))

    def test_stable_order_no_duplicates_across_pages(self):
        page1 = self.client.get(reverse('catalog:list'), {'page': 1, 'sort': 'top'})
        page2 = self.client.get(reverse('catalog:list'), {'page': 2, 'sort': 'top'})
        ids1 = [p.id for p in page1.context['products']]
        ids2 = [p.id for p in page2.context['products']]
        self.assertEqual(len(ids1), CATALOG_PAGE_SIZE)
        self.assertTrue(ids2)
        self.assertEqual(len(set(ids1) & set(ids2)), 0)

    def test_paginate_helper_out_of_range(self):
        qs = Product.objects.on_storefront().order_by('sort_order', 'id')
        products, page = paginate_catalog(qs, '5')
        self.assertEqual(products, [])
        self.assertTrue(page.out_of_range)

    def test_invalid_page_param_defaults_to_first(self):
        resp = self.client.get(reverse('catalog:list'), {'page': 'abc'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['products']), CATALOG_PAGE_SIZE)
