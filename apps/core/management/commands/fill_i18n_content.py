"""Fill empty EN / zh-hans modeltranslation fields from UK originals."""

from __future__ import annotations

import sys
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.translation import override

from apps.booking.models import BookingService
from apps.calculator.models import CalculatorOption, CalculatorQuestion
from apps.catalog.models import Product, ProductReview, ProductVariant
from apps.catalog.models_base import Brand, Category, ProductLine, Tag
from apps.core.block_defaults import is_visibility_key
from apps.core.models import HeroSlide, HistorySlide, SiteBlock, SiteSettings, clear_site_content_cache

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from i18n_content import translate_uk  # noqa: E402


def _uk_value(obj, field: str) -> str:
    for attr in (f'{field}_uk', field):
        val = getattr(obj, attr, None)
        if isinstance(val, str) and val.strip():
            return val.strip()
    raw = obj.__dict__.get(field)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return ''


def _skip_block(obj: SiteBlock, field: str) -> bool:
    if field != 'text_html':
        return False
    if is_visibility_key(obj.key):
        return True
    raw = (getattr(obj, 'text_html_uk', None) or obj.text_html or '').strip()
    return raw in ('0', '1')


class Command(BaseCommand):
    help = 'Заповнює порожні EN/ZH поля CMS і каталогу з українських оригіналів'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписати вже заповнені EN/ZH поля',
        )

    def handle(self, *args, **options):
        force = bool(options.get('force'))
        filled = 0
        missing = 0
        skipped = 0
        jobs = (
            (SiteBlock.objects.all(), ('text_html',), _skip_block),
            (HeroSlide.objects.all(), ('title', 'subtitle', 'cta_primary_label', 'cta_secondary_label'), None),
            (HistorySlide.objects.all(), ('year_label', 'title', 'text', 'cta_label'), None),
            (SiteSettings.objects.all(), ('site_name', 'address', 'work_hours', 'meta_description'), None),
            (Category.objects.all(), ('name', 'description', 'meta_title', 'meta_description'), None),
            (Brand.objects.all(), ('name', 'short_description', 'description', 'country'), None),
            (ProductLine.objects.all(), ('name', 'description'), None),
            (Tag.objects.all(), ('name',), None),
            (
                Product.objects.all(),
                (
                    'name', 'short_story', 'description', 'tasting_notes', 'recommendations',
                    'wrapper', 'binder', 'filler', 'country', 'smoke_time',
                    'meta_title', 'meta_description',
                ),
                None,
            ),
            (ProductVariant.objects.all(), ('name', 'shape'), None),
            (ProductReview.objects.all(), ('text',), None),
            (BookingService.objects.all(), ('title', 'description'), None),
            (CalculatorQuestion.objects.all(), ('title', 'help_text'), None),
            (CalculatorOption.objects.all(), ('label', 'explanation'), None),
        )
        with override('uk'):
            for qs, fields, skipper in jobs:
                for obj in qs:
                    changed: list[str] = []
                    for field in fields:
                        if skipper and skipper(obj, field):
                            skipped += 1
                            continue
                        uk = _uk_value(obj, field)
                        if not uk:
                            continue
                        mapped = translate_uk(uk)
                        if not mapped:
                            missing += 1
                            self.stderr.write(f'  MISSING: {obj.__class__.__name__}.{field} {uk[:90]!r}')
                            continue
                        en, zh = mapped
                        uk_attr = f'{field}_uk'
                        if hasattr(obj, uk_attr) and not (getattr(obj, uk_attr) or '').strip():
                            setattr(obj, uk_attr, uk)
                            changed.append(uk_attr)
                        for lang, val in (('en', en), ('zh_hans', zh)):
                            attr = f'{field}_{lang}'
                            current = (getattr(obj, attr, None) or '').strip()
                            if current and current != uk and not force:
                                continue
                            if current == val:
                                continue
                            setattr(obj, attr, val)
                            changed.append(attr)
                    if changed:
                        obj.save(update_fields=changed)
                        filled += len(changed)
        clear_site_content_cache()
        self.stdout.write(self.style.SUCCESS(
            f'fill_i18n_content: updated_fields={filled}, missing={missing}, skipped={skipped}'
        ))
        if missing:
            self.stderr.write(self.style.ERROR(f'{missing} strings still need a mapping'))
