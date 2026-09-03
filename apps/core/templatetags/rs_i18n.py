"""Helpers for storefront i18n (path localization for CMS CTA URLs)."""

from __future__ import annotations

from django import template
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation.trans_real import get_supported_language_variant

register = template.Library()


def _strip_lang_prefix(path: str) -> str:
    if not path.startswith('/'):
        return path
    parts = path.lstrip('/').split('/', 1)
    if not parts:
        return path
    code = parts[0]
    try:
        get_supported_language_variant(code)
    except LookupError:
        return path
    rest = parts[1] if len(parts) > 1 else ''
    return f'/{rest}' if rest else '/'


@register.filter(name='localize_path')
def localize_path(path: str | None) -> str:
    """Prefix CMS absolute paths with active language (skip default uk)."""
    if not path:
        return ''
    raw = str(path).strip()
    if not raw or raw.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
        return raw
    if not raw.startswith('/'):
        return raw

    lang = get_language() or settings.LANGUAGE_CODE
    clean = _strip_lang_prefix(raw)
    if lang == settings.LANGUAGE_CODE:
        return clean
    if clean == '/':
        return f'/{lang}/'
    return f'/{lang}{clean}'
