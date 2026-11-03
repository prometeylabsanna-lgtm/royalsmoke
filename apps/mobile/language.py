"""Мова текстів мобільного API: ?lang= має пріоритет над Accept-Language, інакше uk."""

from __future__ import annotations

from django.utils import translation
from django.utils.translation.trans_real import parse_accept_lang_header

SUPPORTED = ('uk', 'en', 'zh-hans', 'ms', 'fil', 'id', 'vi')

_PRIMARY = {
    'uk': 'uk',
    'en': 'en',
    'zh': 'zh-hans',
    'ms': 'ms',
    'fil': 'fil',
    'id': 'id',
    'in': 'id',
    'vi': 'vi',
}

_TRADITIONAL = {'zh-hant', 'zh-tw', 'zh-hk', 'zh-mo'}
_SIMPLIFIED = {'zh-hans', 'zh-cn', 'zh-sg'}


def normalize_lang(raw: str) -> str | None:
    code = (raw or '').strip().lower().replace('_', '-')
    if not code:
        return None
    code = code.split(',')[0].split(';')[0].strip()
    if code in _TRADITIONAL:
        return None
    if code in _SIMPLIFIED:
        return 'zh-hans'
    base = code.split('-')[0]
    if base == 'zh':
        return 'zh-hans'
    return _PRIMARY.get(code) or _PRIMARY.get(base)


def resolve_mobile_language(request) -> str:
    query = (request.GET.get('lang') or '').strip()
    if query:
        return normalize_lang(query) or 'uk'
    header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if header:
        for lang, _priority in parse_accept_lang_header(header):
            normalized = normalize_lang(lang)
            if normalized:
                return normalized
    return 'uk'


def activate_mobile_language(request) -> str:
    lang = resolve_mobile_language(request)
    if lang not in SUPPORTED:
        lang = 'uk'
    translation.activate(lang)
    request.LANGUAGE_CODE = lang
    return lang
