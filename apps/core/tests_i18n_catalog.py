"""Сторінка 03 «Каталог і товари»: переклади ms / fil / id / vi з docs/i18n/03-katalog.md."""

import re

from django.test import TestCase

from apps.catalog.models import Product, ProductImage, ProductReview
from apps.catalog.models_base import Brand, Category, ProductLine, Tag
from apps.core.cms_i18n import CMS_LANGUAGES
from apps.core.i18n_audit import CYRILLIC
from apps.core.i18n_testing import SEA_LANGUAGES, TranslationPageMixin, seed_storefront

SEA_ATTRS = [attr for code, attr, _label in CMS_LANGUAGES if code in SEA_LANGUAGES]

FIELDS = {
    Category: ('name', 'description', 'meta_title', 'meta_description'),
    Brand: ('name', 'short_description', 'description', 'country'),
    ProductLine: ('name', 'description'),
    Tag: ('name',),
    Product: (
        'name', 'short_story', 'description', 'tasting_notes', 'recommendations', 'wrapper', 'binder',
        'filler', 'country', 'smoke_time', 'meta_title', 'meta_description',
    ),
    ProductImage: ('alt_text',),
    ProductReview: ('text',),
}


class CatalogTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()

    def _paths(self):
        product = Product.objects.filter(is_active=True).first()
        brand = Brand.objects.first()
        category = Category.objects.first()
        return [
            '/catalog/',
            f'/catalog/product/{product.slug}/',
            f'/catalog/brand/{brand.slug}/',
            f'/catalog/{category.slug}/',
            '/catalog/compare/',
        ]

    def test_no_cyrillic_on_catalog_pages(self):
        for path in self._paths():
            self.assert_no_cyrillic(path)

    def test_search_suggestions_translated(self):
        for lang in SEA_LANGUAGES:
            html = self._html(f'/{lang}/catalog/search/?q=ro', HTTP_HX_REQUEST='true')
            self.assertEqual(self._leftovers(html), [], lang)

    def test_every_table_phrase_is_rendered(self):
        self.assert_phrases_rendered('03-katalog', self._paths(), minimum=100)

    def test_catalog_content_fields_are_filled_in_every_language(self):
        for model, fields in FIELDS.items():
            for obj in model.objects.all():
                for field in fields:
                    uk = getattr(obj, f'{field}_uk') or ''
                    if not CYRILLIC.search(uk):
                        continue
                    for attr in SEA_ATTRS:
                        value = getattr(obj, f'{field}_{attr}') or ''
                        label = f'{model.__name__}#{obj.pk}.{field}_{attr}'
                        self.assertTrue(value.strip(), f'{label} is empty')
                        self.assertNotEqual(value, uk, label)
                        self.assertIsNone(CYRILLIC.search(value), label)

    def test_price_slider_step_follows_currency(self):
        expected = {'ms': 1, 'fil': 1, 'id': 1000, 'vi': 1000}
        for lang, step in expected.items():
            html = self._html(f'/{lang}/catalog/')
            self.assertEqual(set(re.findall(r'data-cb-range-(?:min|max)[^>]*?step="(\d+)"', html, re.S)) or {str(step)},
                             {str(step)}, lang)
            bounds = [int(v) for v in re.findall(r'(?:min|max)="(\d+)"\s+step="%d"' % step, html)]
            self.assertTrue(bounds, lang)
            if step > 1:
                self.assertTrue(all(value % step == 0 for value in bounds), (lang, bounds))

    def test_list_summary_uses_plural_forms(self):
        for lang in SEA_LANGUAGES:
            html = self._html(f'/{lang}/catalog/')
            self.assertRegex(html, r'\d+\s+(?:item|produk|sản phẩm|mga item)', lang)
