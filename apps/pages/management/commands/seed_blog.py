from __future__ import annotations

import sys
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError, no_translations
from modeltranslation.utils import build_localized_fieldname

from apps.pages.blog_seed_bodies1 import POST_BODIES as BODIES_1
from apps.pages.blog_seed_bodies2 import POST_BODIES as BODIES_2
from apps.pages.blog_seed_data import POSTS
from apps.pages.blog_seed_en import BODIES_EN
from apps.pages.blog_seed_extra import EXTRA_UK
from apps.pages.blog_seed_zh import BODIES_ZH
from apps.pages.blog_seed_ms import BODIES as BODIES_MS
from apps.pages.blog_seed_fil import BODIES as BODIES_FIL
from apps.pages.blog_seed_id import BODIES as BODIES_ID
from apps.pages.blog_seed_vi import BODIES as BODIES_VI
from apps.pages.models import BlogFAQItem, BlogPost
from apps.core.block_defaults import BLOCK_CONTENT_TYPES, BLOCK_DEFAULTS, BLOCK_FIELD_LABELS
from apps.core.models import SiteBlock


SEA_CODES = ('ms', 'fil', 'id', 'vi')
SEA_BODIES = {'ms': BODIES_MS, 'fil': BODIES_FIL, 'id': BODIES_ID, 'vi': BODIES_VI}


def _sea(text: str) -> dict[str, str]:
    """Переклад рядка статті з таблиці docs/i18n (scripts/i18n_data)."""
    scripts = Path(__file__).resolve().parents[4] / 'scripts'
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from i18n_sea import translate

    found = translate(text)
    if not found:
        raise CommandError(f'Немає перекладу ms/fil/id/vi: {text[:80]!r}')
    return found


def _put(defaults: dict, field: str, uk: str) -> None:
    found = _sea(uk)
    for code in SEA_CODES:
        defaults[build_localized_fieldname(field, code)] = found[code]


class Command(BaseCommand):
    help = 'Ідемпотентний seed: 4 SEO-статті блогу (UK/EN/ZH і ms/fil/id/vi) з обкладинками'

    @no_translations
    def handle(self, *args, **options):
        self._seed_cms_blocks()
        bodies_uk = {**BODIES_1, **BODIES_2}
        created = updated = 0
        for data in POSTS:
            slug = data['slug']
            body_uk = bodies_uk[slug]['uk'] + EXTRA_UK.get(slug, '')
            body_en = BODIES_EN[slug]
            body_zh = BODIES_ZH[slug]

            defaults = {
                'title': data['title_uk'],
                'title_uk': data['title_uk'],
                'title_en': data['title_en'],
                'title_zh_hans': data['title_zh'],
                'excerpt': data['excerpt_uk'],
                'excerpt_uk': data['excerpt_uk'],
                'excerpt_en': data['excerpt_en'],
                'excerpt_zh_hans': data['excerpt_zh'],
                'body': body_uk,
                'body_uk': body_uk,
                'body_en': body_en,
                'body_zh_hans': body_zh,
                'cover_alt': data['cover_alt_uk'],
                'cover_alt_uk': data['cover_alt_uk'],
                'cover_alt_en': data['cover_alt_en'],
                'cover_alt_zh_hans': data['cover_alt_zh'],
                'meta_title': data['meta_title_uk'],
                'meta_title_uk': data['meta_title_uk'],
                'meta_title_en': data['meta_title_en'],
                'meta_title_zh_hans': data['meta_title_zh'],
                'meta_description': data['meta_description_uk'],
                'meta_description_uk': data['meta_description_uk'],
                'meta_description_en': data['meta_description_en'],
                'meta_description_zh_hans': data['meta_description_zh'],
                **{
                    build_localized_fieldname('body', code): SEA_BODIES[code][slug]
                    for code in SEA_CODES
                },
                'published_at': data['published_at'],
                'is_published': True,
                'sort_order': data['sort_order'],
            }
            for field, uk_key in (
                ('title', 'title_uk'),
                ('excerpt', 'excerpt_uk'),
                ('cover_alt', 'cover_alt_uk'),
                ('meta_title', 'meta_title_uk'),
                ('meta_description', 'meta_description_uk'),
            ):
                _put(defaults, field, data[uk_key])
            post, was_created = BlogPost.objects.update_or_create(
                slug=slug, defaults=defaults,
            )
            self._ensure_cover(post, data['cover'])
            self._sync_faq(post, data['faq'])
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Blog seed: created={created}, updated={updated}',
        ))

    def _seed_cms_blocks(self) -> None:
        keys = [
            ('site', 'nav_blog'),
            ('blog', 'kicker'), ('blog', 'title'), ('blog', 'lead'),
            ('blog', 'meta_description'), ('blog', 'read_more'),
            ('blog', 'back'), ('blog', 'related'),
        ]
        for page, key in keys:
            text = str(BLOCK_DEFAULTS.get((page, key), key))
            SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults={
                    'label': BLOCK_FIELD_LABELS.get((page, key), key),
                    'content_type': BLOCK_CONTENT_TYPES.get((page, key), 'text'),
                    'text_html': text,
                    'is_active': True,
                },
            )
    def _ensure_cover(self, post: BlogPost, rel_path: str) -> None:
        src = Path(settings.BASE_DIR) / rel_path
        if not src.is_file():
            self.stdout.write(self.style.WARNING(f'No cover: {rel_path}'))
            return
        if post.cover:
            post.cover.delete(save=False)
        with src.open('rb') as fh:
            post.cover.save(src.name, File(fh), save=True)

    def _sync_faq(self, post: BlogPost, faq_rows: list[dict]) -> None:
        post.faq_items.all().delete()
        for i, row in enumerate(faq_rows):
            fields = {
                'post': post,
                'sort_order': i * 10,
                'question': row['q_uk'],
                'question_uk': row['q_uk'],
                'question_en': row['q_en'],
                'question_zh_hans': row['q_zh'],
                'answer': row['a_uk'],
                'answer_uk': row['a_uk'],
                'answer_en': row['a_en'],
                'answer_zh_hans': row['a_zh'],
            }
            _put(fields, 'question', row['q_uk'])
            _put(fields, 'answer', row['a_uk'])
            BlogFAQItem.objects.create(**fields)
