"""Helpers for storefront i18n (path localization for CMS CTA URLs)."""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

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


def _prefix_lang(clean_path: str, lang: str) -> str:
    if lang == settings.LANGUAGE_CODE:
        return clean_path
    if clean_path == '/':
        return f'/{lang}/'
    return f'/{lang}{clean_path}'


def localize_path_for(path: str | None, lang: str | None) -> str:
    """Rewrite a storefront path (and optional query) for the target language."""
    if not path:
        return '/'
    raw = str(path).strip()
    if not raw:
        return '/'
    parsed = urlsplit(raw)
    path_only = parsed.path or '/'
    if not path_only.startswith('/'):
        path_only = f'/{path_only}'
    new_path = _prefix_lang(_strip_lang_prefix(path_only), lang or settings.LANGUAGE_CODE)
    return urlunsplit((parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment))


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
    return localize_path_for(raw, get_language() or settings.LANGUAGE_CODE)


@register.simple_tag
def storefront_languages() -> dict:
    """Мови для перемикача: видимі (STOREFRONT_LANGUAGES_VISIBLE) + поточна, навіть якщо вона прихована."""
    current = get_language() or settings.LANGUAGE_CODE
    visible = set(getattr(settings, 'STOREFRONT_LANGUAGES_VISIBLE', ())) | {current}
    names = dict(settings.LANGUAGES)
    short = getattr(settings, 'LANGUAGE_SHORT_LABELS', {})
    entries = [
        {
            'code': code,
            'name': names[code],
            'short': short.get(code, code.upper()),
            'is_current': code == current,
        }
        for code, _name in settings.LANGUAGES
        if code in visible
    ]
    current_entry = next((e for e in entries if e['is_current']), entries[0] if entries else None)
    return {'entries': entries, 'current': current_entry}


@register.simple_tag(takes_context=True)
def language_next(context, lang_code: str) -> str:
    request = context.get('request')
    current = request.get_full_path() if request is not None else '/'
    return localize_path_for(current, lang_code)
