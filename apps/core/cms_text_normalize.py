"""Нормалізація CMS-текстів після TinyMCE (без видимих тегів на вітрині)."""

from __future__ import annotations

import re

from django.utils.html import strip_tags
from django.utils.safestring import SafeString, mark_safe

# Поля SiteBlock, які навмисно зберігають HTML і рендеряться через |safe / cms_html.
CMS_RICH_HTML_KEYS = frozenset({'body'})

_BR_RE = re.compile(r'<br\s*/?>', re.IGNORECASE)
_P_CLOSE_RE = re.compile(r'</p\s*>', re.IGNORECASE)
_BLOCK_OPEN_RE = re.compile(r'<(p|div|li|h[1-6])\b[^>]*>', re.IGNORECASE)


def normalize_cms_plain(value: str | None) -> str:
    """Прибирає обгортки TinyMCE (<p>, <br>) → звичайний текст для лейблів/лідів."""
    text = (value or '').strip()
    if not text:
        return ''
    text = _BR_RE.sub('\n', text)
    text = _P_CLOSE_RE.sub('\n', text)
    text = strip_tags(text)
    lines = [ln.strip() for ln in text.replace('\r\n', '\n').split('\n')]
    return '\n'.join(ln for ln in lines if ln)


def cms_display_value(key: str, value: str | None) -> str | SafeString:
    """Для вітрини: plain для звичайних ключів, HTML для body."""
    raw = (value or '').strip()
    if not raw:
        return ''
    if key in CMS_RICH_HTML_KEYS:
        return mark_safe(raw)
    return normalize_cms_plain(raw)


def sanitize_cms_storage(key: str, value: str | None) -> str:
    """При збереженні з адмінки: не-HTML ключі без тегів; body лишаємо як є."""
    raw = (value or '').strip()
    if not raw:
        return ''
    if key in CMS_RICH_HTML_KEYS:
        return raw
    return normalize_cms_plain(raw)
