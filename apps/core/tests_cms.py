from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.block_defaults import BLOCK_DEFAULTS, is_visibility_key
from apps.core.models import PageStyle, SiteBlock, SiteSettings
from apps.core.page_styles import ensure_page_styles
from apps.core.site_content_registry import get_section, iter_section_blocks
from apps.core.site_content_sections import CONTENT_SECTIONS
from apps.pages.models import FAQItem, LegalDocument


class CmsRegistryTests(TestCase):
    def test_unique_page_key_pairs(self):
        pairs = []
        for section in CONTENT_SECTIONS:
            for pair in iter_section_blocks(section):
                pairs.append(pair)
        self.assertEqual(len(pairs), len(set(pairs)))

    def test_unique_admin_model_names(self):
        names = [s.admin_model_name for s in CONTENT_SECTIONS if s.admin_model_name]
        self.assertEqual(len(names), len(set(names)))

    def test_visibility_keys_are_in_iter(self):
        for section in CONTENT_SECTIONS:
            if not section.visibility_key:
                continue
            keys = {key for _page, key in iter_section_blocks(section)}
            self.assertIn(section.visibility_key, keys)


class CmsAdminTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='cms@test.ua', password='pass12345',
        )
        self.client.force_login(self.user)
        SiteSettings.load()

    def test_hero_section_get(self):
        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UA')
        self.assertContains(response, 'data-cms-langs')

    def test_post_updates_uk_text(self):
        url = reverse('admin:core_homeherosettings_change', args=[1])
        self.client.get(url)
        payload = {
            'section_visible': 'on',
            'block__home__hero_eyebrow__text_html_uk': 'Atelier Test',
            'block__home__hero_eyebrow__text_html_en': 'Atelier EN',
            'block__home__hero_eyebrow__text_html_zh_hans': '工坊',
            'hero_slides-TOTAL_FORMS': '0',
            'hero_slides-INITIAL_FORMS': '0',
            'hero_slides-MIN_NUM_FORMS': '0',
            'hero_slides-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        block = SiteBlock.objects.get(page='home', key='hero_eyebrow')
        self.assertEqual(block.text_html_uk, 'Atelier Test')
        self.assertEqual(block.text_html_en, 'Atelier EN')

    def test_header_toggle_off(self):
        section = get_section('home', 'hero')
        self.assertTrue(is_visibility_key(section.visibility_key))
        url = reverse('admin:core_homeherosettings_change', args=[1])
        self.client.get(url)
        payload = {
            'block__home__hero_eyebrow__text_html_uk': 'x',
            'block__home__hero_eyebrow__text_html_en': '',
            'block__home__hero_eyebrow__text_html_zh_hans': '',
            'hero_slides-TOTAL_FORMS': '0',
            'hero_slides-INITIAL_FORMS': '0',
            'hero_slides-MIN_NUM_FORMS': '0',
            'hero_slides-MAX_NUM_FORMS': '1000',
        }
        self.client.post(url, payload)
        vis = SiteBlock.objects.get(page='home', key='hero_section_visible')
        self.assertEqual(vis.text_html, '0')

    def test_history_slide_shows_image_preview(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from apps.core.models import HistorySlide

        png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
            b'\r\n\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        slide = HistorySlide.objects.create(
            title='Slide',
            image=SimpleUploadedFile('hist.png', png, content_type='image/png'),
            sort_order=0,
            is_active=True,
        )
        url = reverse('admin:core_homeaboutsettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-cms-image-preview')
        self.assertContains(response, slide.image.name)
        self.assertContains(response, 'rs-cms-image__frame')

    def test_hero_slide_shows_image_preview(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from apps.core.models import HeroSlide

        png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
            b'\r\n\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        slide = HeroSlide.objects.create(
            title='Hero',
            image=SimpleUploadedFile('hero.png', png, content_type='image/png'),
            sort_order=0,
            is_active=True,
        )
        url = reverse('admin:core_homeherosettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-cms-image-preview')
        self.assertContains(response, slide.image.name)
        self.assertContains(response, 'rs-cms-image__frame')

    def test_category_form_uses_image_widget(self):
        from apps.catalog.models_base import Category

        cat = Category.objects.create(name='Cigars', slug='cigars-preview-test')
        response = self.client.get(reverse('admin:catalog_category_change', args=[cat.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-cms-image')
        self.assertContains(response, 'accept="image/*"')


class CmsFrontendTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        for (page, key), text in BLOCK_DEFAULTS.items():
            SiteBlock.objects.get_or_create(
                page=page, key=key,
                defaults={'label': key, 'text_html': str(text), 'is_active': True},
            )

    def test_faq_admin_has_lang_switcher(self):
        item = FAQItem.objects.create(question='Q1', answer='A1', sort_order=0, is_active=True)
        User = get_user_model()
        user = User.objects.create_superuser(email='faq@test.ua', password='pass12345')
        self.client.force_login(user)
        response = self.client.get(reverse('admin:pages_faqitem_change', args=[item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'question_uk')
        self.assertContains(response, 'question_en')
        self.assertContains(response, 'question_zh_hans')
        self.assertContains(response, 'cms_lang_switch.js')

    def test_faq_renders_items(self):
        FAQItem.objects.create(question='Q1', answer='A1', sort_order=0, is_active=True)
        response = self.client.get(reverse('pages:faq'))
        self.assertContains(response, 'Q1')
        self.assertContains(response, 'A1')

    def test_legal_renders_body(self):
        LegalDocument.objects.create(
            slug='privacy', title='Privacy', body='<p>Secret</p>', is_active=True,
        )
        response = self.client.get(reverse('pages:legal', kwargs={'slug': 'privacy'}))
        self.assertContains(response, 'Secret')


class PageStyleTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='style@test.ua', password='pass12345',
        )
        self.client.force_login(self.user)
        ensure_page_styles()

    def test_ensure_creates_all_pages(self):
        self.assertEqual(PageStyle.objects.count(), len(SiteBlock.Page.choices))

    def test_reset_clears_color(self):
        style = PageStyle.objects.get(page='home')
        style.background_color = '#221100'
        style.text_color = '#abcdef'
        style.accent_color = '#112233'
        style.save()
        style.reset_to_default()
        style.refresh_from_db()
        self.assertEqual(style.background_color, '')
        self.assertEqual(style.text_color, '')
        self.assertEqual(style.accent_color, '')
        self.assertEqual(style.effective_background, PageStyle.DEFAULT_BACKGROUND)

    def test_admin_reset_button(self):
        style = PageStyle.objects.get(page='about')
        style.background_color = '#334455'
        style.save()
        url = reverse('admin:core_pagestyle_change', args=[style.pk])
        response = self.client.post(url, {
            'background_color': '#334455',
            'text_color': '#fcf2ee',
            'accent_color': '#c99a44',
            '_reset_default': '1',
        })
        self.assertEqual(response.status_code, 302)
        style.refresh_from_db()
        self.assertEqual(style.background_color, '')

    def test_frontend_applies_custom_bg(self):
        style = PageStyle.objects.get(page='home')
        style.background_color = '#1a1512'
        style.text_color = '#eeddcc'
        style.accent_color = '#aabb00'
        style.save()
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '--rs-page-bg: #1a1512')
        self.assertContains(response, '--rs-page-text: #eeddcc')
        self.assertContains(response, '--rs-page-accent: #aabb00')

    def test_admin_has_circle_picker_and_preview(self):
        style = PageStyle.objects.get(page='about')
        url = reverse('admin:core_pagestyle_change', args=[style.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rs-cms-colorpick')
        self.assertContains(response, 'data-cms-color-circle')
        self.assertContains(response, 'data-cms-color-default')
        self.assertContains(response, 'Дефолт')
        self.assertContains(response, 'data-default-color="#fcf2ee"')
        self.assertContains(response, 'data-default-color="#c99a44"')
        self.assertContains(response, 'Подивитись на сайті')
        self.assertContains(response, 'data-page-style-preview')
        self.assertContains(response, 'text_color')
        self.assertContains(response, 'accent_color')

    def test_preview_query_without_login(self):
        self.client.logout()
        response = self.client.get(
            reverse('pages:about')
            + '?rs_style_preview=1&preview_bg=%23eb3b00&preview_text=%23100d0c&preview_accent=%23c99a44',
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '--rs-page-bg: #eb3b00')
        self.assertContains(response, 'is-style-preview')
        self.assertContains(response, 'Превʼю кольорів')


class CmsTinyMCETests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='tinymce@test.ua', password='pass12345',
        )
        self.client.force_login(self.user)
        SiteSettings.load()

    def test_service_section_uses_tinymce_for_leads(self):
        url = reverse('admin:core_homeservicesettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tinymce')

    def test_faq_answer_uses_tinymce(self):
        item = FAQItem.objects.create(question='Q', answer='A', sort_order=0)
        response = self.client.get(reverse('admin:pages_faqitem_change', args=[item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tinymce')


class DeliveryCardsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='delivery@test.ua', password='pass12345',
        )
        self.client.force_login(self.user)
        SiteSettings.load()

    def test_seed_and_frontend(self):
        from apps.core.delivery_cards import ensure_delivery_cards
        from apps.core.models import DeliveryCard

        ensure_delivery_cards()
        self.assertEqual(
            DeliveryCard.objects.filter(kind=DeliveryCard.Kind.REGION).count(), 4,
        )
        self.assertEqual(
            DeliveryCard.objects.filter(kind=DeliveryCard.Kind.PAYMENT).count(), 3,
        )
        response = self.client.get(reverse('leads:delivery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Київ')
        self.assertContains(response, 'Онлайн оплата')

    def test_admin_shows_formsets(self):
        from apps.core.delivery_cards import ensure_delivery_cards

        ensure_delivery_cards()
        url = reverse('admin:core_deliverypagesettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'delivery_regions')
        self.assertContains(response, 'delivery_payments')
        self.assertContains(response, 'Картки доставки')
        self.assertNotContains(response, 'kyiv_title')
