from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.block_defaults import BLOCK_DEFAULTS, is_visibility_key
from apps.core.models import SiteBlock, SiteSettings
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
        HistorySlide.objects.create(
            title='Slide',
            image=SimpleUploadedFile('hist.png', png, content_type='image/png'),
            sort_order=0,
            is_active=True,
        )
        url = reverse('admin:core_homeaboutsettings_change', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-cms-image-preview')
        self.assertContains(response, 'hist.png')

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
