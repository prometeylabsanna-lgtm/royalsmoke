"""Тексти карток брендів на головній: канонічний український абзац і переклади таблиці.

Порожня колонка мови в modeltranslation підставляє англійську, потім українську.
На проді після старого деплою колонки ms/fil/id/vi часто порожні, тож опис лишається
англійським, хоча кнопки з gettext уже перекладені. Вітрина бере текст із таблиці.
"""

from __future__ import annotations

import sys
from pathlib import Path

from django.utils.translation import get_language
from modeltranslation.utils import build_localized_fieldname

from apps.core.block_defaults import BRAND_CARD_TEXT_DEFAULTS, BRAND_IMAGE_FALLBACKS

_SCRIPTS = Path(__file__).resolve().parents[2] / 'scripts'
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from i18n_content import translate_uk  # noqa: E402
from i18n_sea import translate as translate_sea  # noqa: E402


def render_translation(uk: str) -> str:
    """Абзац українською → текст активної мови вітрини. Немає збігу — український оригінал."""
    raw = (uk or '').strip()
    if not raw:
        return ''
    lang = get_language() or 'uk'
    if lang == 'uk':
        return raw
    if lang in ('en', 'zh-hans'):
        mapped = translate_uk(raw)
        if not mapped:
            return raw
        return mapped[0] if lang == 'en' else mapped[1]
    sea = translate_sea(raw) or {}
    return (sea.get(lang) or raw).strip()


def home_brand_description(brand, card=None) -> str:
    """Опис на головній. Для чотирьох відомих брендів — затверджений текст таблиці."""
    canonical = BRAND_CARD_TEXT_DEFAULTS.get(getattr(brand, 'slug', '') or '', '')
    if canonical:
        return render_translation(canonical)
    if card is not None:
        text = (getattr(card, 'text', None) or '').strip()
        if text:
            return text
    return (getattr(brand, 'short_description', None) or getattr(brand, 'description', None) or '').strip()


def _write_field(obj, field: str, uk: str) -> None:
    mapped = translate_uk(uk)
    values: dict[str, str] = {'uk': uk}
    if mapped:
        values['en'], values['zh-hans'] = mapped
    sea = translate_sea(uk) or {}
    values.update(sea)
    update: list[str] = []
    for lang, val in values.items():
        attr = build_localized_fieldname(field, lang)
        if (getattr(obj, attr, None) or '') != val:
            setattr(obj, attr, val)
            update.append(attr)
    if update:
        obj.save(update_fields=update)


def sync_brand_blurbs(brand, card, uk: str) -> None:
    """Записати український абзац і переклади в бренд і картку головної."""
    text = (uk or '').strip()
    if not text:
        return
    _write_field(brand, 'short_description', text)
    _write_field(card, 'text', text)


def seed_brand_cards() -> None:
    from pathlib import Path as FsPath

    from django.conf import settings
    from django.core.files import File

    from apps.catalog.models_base import Brand
    from apps.core.models import HomeBrandCard

    brands = list(Brand.objects.filter(is_featured=True).order_by('sort_order', 'id')[:4])
    if not brands:
        brands = list(Brand.objects.filter(is_active=True).order_by('sort_order', 'id')[:4])
    static_root = FsPath(settings.BASE_DIR) / 'static'
    for i, brand in enumerate(brands):
        text = BRAND_CARD_TEXT_DEFAULTS.get(brand.slug, '')
        card, _created = HomeBrandCard.objects.get_or_create(
            brand=brand,
            defaults={'sort_order': i, 'is_active': True},
        )
        if card.sort_order != i or not card.is_active:
            card.sort_order = i
            card.is_active = True
            card.save(update_fields=['sort_order', 'is_active'])
        rel = BRAND_IMAGE_FALLBACKS.get(brand.slug)
        path = static_root / rel if rel else None
        if path is not None and path.is_file():
            with path.open('rb') as fh:
                card.image.save(path.name, File(fh), save=True)
        if text:
            sync_brand_blurbs(brand, card, text)
