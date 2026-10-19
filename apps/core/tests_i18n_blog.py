"""Сторінка 08 «Блог»: переклади ms / fil / id / vi з docs/i18n/08-blog.md."""

from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from apps.core.i18n_testing import SEA_LANGUAGES, TranslationPageMixin, seed_storefront
from apps.pages.models import BlogPost


class BlogTranslationTests(TranslationPageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_storefront()
        call_command('seed_blog', stdout=StringIO())
        call_command('fill_i18n_content', stdout=StringIO(), stderr=StringIO())

    def test_push_permission_bar_is_gone(self):
        source = (Path(settings.BASE_DIR) / 'static/js/pwa.js').read_text(encoding='utf-8')
        self.assertNotIn('rs-pwa-push-bar', source)
        self.assertNotIn('showPushPrompt', source)

    def test_list_and_articles_have_no_cyrillic(self):
        self.assert_no_cyrillic('/blog/')
        for slug in BlogPost.objects.values_list('slug', flat=True):
            self.assert_no_cyrillic(f'/blog/{slug}/')

    def test_article_bodies_follow_ukrainian_structure(self):
        for post in BlogPost.objects.all():
            uk_blocks = post.body_uk.count('<h2') + post.body_uk.count('<p') + post.body_uk.count('<li')
            for lang, attr in (('ms', 'body_ms'), ('fil', 'body_fil'), ('id', 'body_ind'), ('vi', 'body_vi')):
                html = getattr(post, attr)
                self.assertTrue(html, f'{post.slug} {lang}')
                same = html.count('<h2') + html.count('<p') + html.count('<li')
                self.assertEqual(same, uk_blocks, f'{post.slug} {lang}')
                self.assertNotIn('href="/catalog/', html)
                self.assertIn(f'href="/{lang}/', html)

    def test_vietnamese_article_title(self):
        html = self._html('/vi/blog/yak-obraty-pershu-sygaru/')
        self.assertIn('Cách chọn điếu xì gà đầu tiên', html)
        self.assertNotIn('Як обрати першу сигару', html)

    def test_list_phrases_are_rendered(self):
        self.assert_phrases_rendered('08-blog', ['/blog/'], minimum=8)
        self.assertGreaterEqual(len(SEA_LANGUAGES), 4)
