"""Етап 0 інтеграції ms / fil / id / vi: налаштування, схема, каталоги, валюти, адмінка."""

from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import check_for_language, get_language_info
from modeltranslation.utils import build_localized_fieldname

from apps.catalog.models import Product
from apps.catalog.models_base import Brand, Category, Tag
from apps.core.cms_i18n import CMS_LANGUAGES, lang_field_set, lang_fields
from apps.core.currency import (
    clear_currency_cache,
    convert_cart_totals,
    convert_from_uah,
    language_currency_code,
    round_for_currency,
)
from apps.core.models import CurrencyRate, SiteBlock
from apps.core.templatetags.rs_i18n import localize_path_for

SEA = ('ms', 'fil', 'id', 'vi')


class LanguageSettingsTests(TestCase):
    def test_all_storefront_languages_registered(self):
        codes = [code for code, _name in settings.LANGUAGES]
        self.assertEqual(codes, ['uk', 'en', 'zh-hans', 'ms', 'fil', 'id', 'vi'])
        self.assertEqual(tuple(codes), tuple(settings.MODELTRANSLATION_LANGUAGES))

    def test_visible_languages_are_a_subset(self):
        codes = {code for code, _name in settings.LANGUAGES}
        self.assertTrue(set(settings.STOREFRONT_LANGUAGES_VISIBLE) <= codes)

    def test_filipino_language_info(self):
        info = get_language_info('fil')
        self.assertEqual(info['code'], 'fil')
        self.assertEqual(info['name_local'], 'Filipino')
        self.assertFalse(info['bidi'])

    def test_catalogs_exist_for_every_language(self):
        for code in ('uk', 'en', 'zh-hans', *SEA):
            self.assertTrue(check_for_language(code), code)

    def test_language_prefix_helpers(self):
        for code in SEA:
            self.assertEqual(localize_path_for('/catalog/', code), f'/{code}/catalog/')
            self.assertEqual(localize_path_for(f'/{code}/catalog/', 'uk'), '/catalog/')
            self.assertEqual(localize_path_for('/', code), f'/{code}/')

    def test_storefront_pages_open_in_every_language(self):
        for code in ('uk', 'en', 'zh-hans', *SEA):
            with translation.override(code):
                url = reverse('pages:home')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, (code, url))
            self.assertEqual(response.context['request'].LANGUAGE_CODE, code)


class ModelTranslationSchemaTests(TestCase):
    def test_indonesian_suffix_is_ind(self):
        self.assertEqual(build_localized_fieldname('name', 'id'), 'name_ind')
        self.assertTrue(dict((code, attr) for code, attr, _l in CMS_LANGUAGES)['id'] == 'ind')

    def test_cms_attrs_match_modeltranslation(self):
        for code, attr, _label in CMS_LANGUAGES:
            self.assertEqual(build_localized_fieldname('name', code), f'name_{attr}')

    def test_new_columns_exist_on_models(self):
        for model, field in ((Product, 'name'), (Brand, 'name'), (Category, 'name'), (Tag, 'name')):
            for code, attr, _label in CMS_LANGUAGES:
                self.assertTrue(hasattr(model, f'{field}_{attr}'), (model, field, attr))
        self.assertTrue(hasattr(SiteBlock, 'text_html_ind'))

    def test_lang_field_helpers(self):
        self.assertEqual(lang_fields('title')[:3], ('title_uk', 'title_en', 'title_zh_hans'))
        self.assertEqual(len(lang_fields('title', 'text')), 2 * len(CMS_LANGUAGES))
        self.assertIn('body', lang_field_set('body'))
        self.assertIn('body_ind', lang_field_set('body'))

    def test_new_language_falls_back_to_english_then_ukrainian(self):
        tag = Tag.objects.create(name_uk='Тест', name_en='Test', slug='test')
        with translation.override('vi'):
            self.assertEqual(Tag.objects.get(pk=tag.pk).name, 'Test')
        tag2 = Tag.objects.create(name_uk='Лише укр', slug='only-uk')
        with translation.override('fil'):
            self.assertEqual(Tag.objects.get(pk=tag2.pk).name, 'Лише укр')
        with translation.override('en'):
            self.assertEqual(Tag.objects.get(pk=tag2.pk).name, 'Лише укр')

    def test_translation_value_is_stored_per_language(self):
        tag = Tag.objects.create(name_uk='Горіх', slug='nut')
        tag.name_ind = 'Kacang'
        tag.name_ms = 'Kacang ms'
        tag.save()
        tag.refresh_from_db()
        with translation.override('id'):
            self.assertEqual(tag.name, 'Kacang')
        with translation.override('ms'):
            self.assertEqual(tag.name, 'Kacang ms')


class SeaCurrencyTests(TestCase):
    def setUp(self):
        clear_currency_cache()

    def test_language_currency_mapping(self):
        expected = {'ms': 'MYR', 'fil': 'PHP', 'id': 'IDR', 'vi': 'VND'}
        for lang, code in expected.items():
            self.assertEqual(language_currency_code(lang), code)

    def test_rate_rows_seeded_with_precise_rates(self):
        for code in ('MYR', 'PHP', 'IDR', 'VND'):
            self.assertTrue(CurrencyRate.objects.filter(code=code).exists(), code)
        idr = CurrencyRate.objects.get(code='IDR')
        self.assertEqual(idr.uah_per_unit, Decimal('0.00250000'))
        self.assertEqual(idr.symbol, 'Rp')

    def test_rate_precision_survives_save(self):
        vnd = CurrencyRate.objects.get(code='VND')
        vnd.uah_per_unit = Decimal('0.00157834')
        vnd.save()
        vnd.refresh_from_db()
        self.assertEqual(vnd.uah_per_unit, Decimal('0.00157834'))

    def test_zero_decimal_currencies_are_whole_numbers(self):
        self.assertEqual(convert_from_uah(Decimal('1000'), 'IDR'), Decimal('400000'))
        self.assertEqual(str(convert_from_uah(Decimal('1000'), 'IDR')), '400000')
        self.assertEqual(str(convert_from_uah(Decimal('1000'), 'VND')), '641026')
        self.assertEqual(round_for_currency(Decimal('10.5'), 'VND'), Decimal('11'))
        self.assertEqual(round_for_currency(Decimal('10.555'), 'MYR'), Decimal('10.56'))

    def test_two_decimal_currencies_keep_cents(self):
        self.assertEqual(convert_from_uah(Decimal('1000'), 'MYR'), Decimal('102.46'))
        self.assertEqual(convert_from_uah(Decimal('1000'), 'PHP'), Decimal('1428.57'))
        self.assertEqual(convert_from_uah(Decimal('1000'), 'UAH'), Decimal('1000.00'))

    def test_cart_totals_in_idr_have_no_fraction(self):
        totals = {
            'items': [{'unit_price': Decimal('1250.50'), 'quantity': 2}],
            'discount': Decimal('0'),
        }
        with translation.override('id'):
            priced = convert_cart_totals(totals, Decimal('100'))
        self.assertEqual(priced['currency'], 'IDR')
        for key in ('subtotal', 'delivery_cost', 'discount', 'total'):
            self.assertEqual(priced[key], priced[key].to_integral_value(), key)
        self.assertNotIn('.', str(priced['total']))
        self.assertEqual(priced['total'], priced['subtotal'] + priced['delivery_cost'] - priced['discount'])


class AdminLanguageTabsTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_superuser(email='sea@test.ua', password='pass12345')
        self.client.force_login(user)

    def test_product_admin_shows_new_language_fields(self):
        response = self.client.get(reverse('admin:catalog_product_add'))
        self.assertEqual(response.status_code, 200)
        for attr in ('ms', 'fil', 'ind', 'vi'):
            self.assertContains(response, f'name="description_{attr}"')

    def test_blog_admin_shows_new_language_fields(self):
        response = self.client.get(reverse('admin:pages_blogpost_add'))
        self.assertEqual(response.status_code, 200)
        for attr in ('ms', 'fil', 'ind', 'vi'):
            self.assertContains(response, f'name="title_{attr}"')

    def test_currency_admin_lists_new_rates(self):
        response = self.client.get(reverse('admin:core_currencyrate_changelist'))
        self.assertEqual(response.status_code, 200)
        for code in ('MYR', 'PHP', 'IDR', 'VND'):
            self.assertContains(response, code)


class LanguageSwitcherTests(TestCase):
    def _home(self, path='/'):
        return self.client.get(path).content.decode()

    def test_header_has_dropdown_with_visible_languages_only(self):
        html = self._home()
        self.assertIn('data-lang-menu', html)
        self.assertIn('English', html)
        self.assertIn('hreflang="en"', html)
        self.assertIn('hreflang="zh-hans"', html)
        for hidden in ('Bahasa Melayu', 'Filipino', 'Bahasa Indonesia', 'Tiếng Việt'):
            self.assertNotIn(hidden, html)

    def test_drawer_uses_inline_list(self):
        html = self._home()
        self.assertIn('rs-lang rs-lang--list', html)

    def test_hidden_current_language_is_still_listed(self):
        html = self._home('/vi/')
        self.assertIn('Tiếng Việt', html)
        self.assertIn('aria-current="true"', html)

    def test_enabling_a_language_adds_it_to_the_switcher(self):
        visible = (*settings.STOREFRONT_LANGUAGES_VISIBLE, 'ms', 'fil', 'id', 'vi')
        with self.settings(STOREFRONT_LANGUAGES_VISIBLE=visible):
            html = self._home()
        for name in ('Bahasa Melayu', 'Filipino', 'Bahasa Indonesia', 'Tiếng Việt'):
            self.assertIn(name, html)
        for code in ('ms', 'fil', 'id', 'vi'):
            self.assertIn(f'href="/{code}/"', html)


class PwaLanguageListsTests(TestCase):
    """JS не читає settings, тож списки мов у файлах мають збігатися з settings.LANGUAGES."""

    def _prefixed(self):
        return [code for code, _name in settings.LANGUAGES if code != settings.LANGUAGE_CODE]

    def _declared(self, relative_path):
        import re
        from pathlib import Path

        text = (Path(settings.BASE_DIR) / relative_path).read_text(encoding='utf-8')
        match = re.search(r"PREFIXED_LANGS\s*=\s*\[([^\]]*)\]", text)
        self.assertIsNotNone(match, relative_path)
        return re.findall(r"'([^']+)'", match.group(1))

    def test_offline_catalog_js_matches_settings(self):
        self.assertEqual(self._declared('static/js/pwa-offline-catalog.js'), self._prefixed())

    def test_service_worker_matches_settings(self):
        self.assertEqual(self._declared('templates/pwa/sw.js'), self._prefixed())

    def test_admin_tabs_js_matches_settings(self):
        import re
        from pathlib import Path

        text = (Path(settings.BASE_DIR) / 'static/js/admin/cms_lang_switch.js').read_text(encoding='utf-8')
        codes = re.findall(r'\{ code: "([^"]+)", suffix: "([^"]+)"', text)
        self.assertEqual(
            codes,
            [(code, attr) for code, attr, _label in CMS_LANGUAGES],
        )


class SeedLanguageIndependenceTests(TestCase):
    """seed_demo не залежить від активної мови: українські тексти не потрапляють у *_vi."""

    def test_seed_demo_under_leaked_language_keeps_vi_empty(self):
        from io import StringIO

        from django.core.management import call_command

        translation.activate('vi')
        self.addCleanup(translation.deactivate)
        call_command('seed_demo', stdout=StringIO())
        brand = Brand.objects.filter(country_uk='Мексика').first()
        self.assertIsNotNone(brand)
        self.assertFalse(brand.country_vi)
        self.assertEqual(brand.country_uk, 'Мексика')
