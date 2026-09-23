from __future__ import annotations

import re
from urllib.parse import urlencode

from django.core.cache import cache
from django.urls import reverse

from apps.core.models import PageStyle, SiteBlock, clear_site_content_cache

PAGE_STYLES_CACHE_KEY = 'page_styles'
_HEX_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

# (namespace, url_name) → SiteBlock.Page value
_URL_PAGE_MAP: dict[tuple[str | None, str | None], str] = {
    ('pages', 'home'): SiteBlock.Page.HOME,
    ('pages', 'about'): SiteBlock.Page.ABOUT,
    ('pages', 'blog'): SiteBlock.Page.BLOG,
    ('pages', 'blog_detail'): SiteBlock.Page.BLOG,
    ('pages', 'faq'): SiteBlock.Page.FAQ,
    ('pages', 'legal'): SiteBlock.Page.SITE,
    ('pages', 'age_gate'): SiteBlock.Page.AGE,
    ('catalog', 'list'): SiteBlock.Page.CATALOG,
    ('catalog', 'category'): SiteBlock.Page.CATALOG,
    ('catalog', 'brand'): SiteBlock.Page.CATALOG,
    ('catalog', 'product'): SiteBlock.Page.CATALOG,
    ('catalog', 'compare'): SiteBlock.Page.CATALOG,
    ('catalog', 'search'): SiteBlock.Page.CATALOG,
    ('leads', 'contact'): SiteBlock.Page.CONTACT,
    ('leads', 'delivery'): SiteBlock.Page.DELIVERY,
    ('leads', 'b2b'): SiteBlock.Page.B2B,
    ('booking', 'page'): SiteBlock.Page.BOOKING,
    ('cart', 'detail'): SiteBlock.Page.CART,
    ('orders', 'checkout'): SiteBlock.Page.CHECKOUT,
    ('accounts', 'cabinet'): SiteBlock.Page.CABINET,
    ('accounts', 'wishlist'): SiteBlock.Page.CABINET,
    ('calculator', 'page'): SiteBlock.Page.HOME,
    ('calculator', 'results'): SiteBlock.Page.HOME,
}

_PAGE_PREVIEW_REVERSE: dict[str, tuple[str, dict]] = {
    SiteBlock.Page.HOME: ('pages:home', {}),
    SiteBlock.Page.ABOUT: ('pages:about', {}),
    SiteBlock.Page.BLOG: ('pages:blog', {}),
    SiteBlock.Page.FAQ: ('pages:faq', {}),
    SiteBlock.Page.CONTACT: ('leads:contact', {}),
    SiteBlock.Page.DELIVERY: ('leads:delivery', {}),
    SiteBlock.Page.B2B: ('leads:b2b', {}),
    SiteBlock.Page.BOOKING: ('booking:page', {}),
    SiteBlock.Page.CATALOG: ('catalog:list', {}),
    SiteBlock.Page.CART: ('cart:detail', {}),
    SiteBlock.Page.CHECKOUT: ('orders:checkout', {}),
    SiteBlock.Page.CABINET: ('accounts:cabinet', {}),
    SiteBlock.Page.AGE: ('pages:home', {}),
    SiteBlock.Page.SITE: ('pages:home', {}),
    SiteBlock.Page.SERVICE: ('pages:home', {}),
}


def ensure_page_styles() -> int:
    created = 0
    for value, _label in SiteBlock.Page.choices:
        _, was_created = PageStyle.objects.get_or_create(
            page=value,
            defaults={
                'background_color': '',
                'text_color': '',
                'accent_color': '',
            },
        )
        if was_created:
            created += 1
    if created:
        clear_site_content_cache()
    return created


def resolve_page_key(request) -> str | None:
    match = getattr(request, 'resolver_match', None)
    if match is None:
        return None
    return _URL_PAGE_MAP.get((match.namespace, match.url_name))


def normalize_hex(value: str, *, default: str = '') -> str:
    raw = (value or '').strip()
    if not raw:
        return default
    if not _HEX_RE.match(raw):
        return default
    if len(raw) == 4:
        return f'#{raw[1] * 2}{raw[2] * 2}{raw[3] * 2}'.lower()
    return raw.lower()


def page_preview_url(page: str) -> str:
    tip = _PAGE_PREVIEW_REVERSE.get(page, ('pages:home', {}))
    name, kwargs = tip
    try:
        return reverse(name, kwargs=kwargs)
    except Exception:
        return '/'


def _styles_map() -> dict[str, dict[str, str]]:
    cached = cache.get(PAGE_STYLES_CACHE_KEY)
    if cached is not None:
        return cached
    data: dict[str, dict[str, str]] = {}
    for row in PageStyle.objects.all():
        data[row.page] = {
            'bg': (row.background_color or '').strip(),
            'text': (row.text_color or '').strip(),
            'accent': (row.accent_color or '').strip(),
        }
    cache.set(PAGE_STYLES_CACHE_KEY, data, 300)
    return data


def _preview_from_request(request) -> dict[str, str]:
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}
    if not (request.user.is_staff or request.user.is_superuser):
        return {}
    if request.GET.get('rs_style_preview') != '1':
        return {}
    return {
        'bg': normalize_hex(request.GET.get('preview_bg', '')),
        'text': normalize_hex(request.GET.get('preview_text', '')),
        'accent': normalize_hex(request.GET.get('preview_accent', '')),
    }


def get_page_style_vars(request) -> dict[str, str]:
    """Повертає кастомні CSS-змінні (порожні = дефолт CSS)."""
    preview = _preview_from_request(request)
    if preview and any(preview.values()):
        return {
            'bg': preview.get('bg', ''),
            'text': preview.get('text', ''),
            'accent': preview.get('accent', ''),
            'is_preview': True,
        }

    page = resolve_page_key(request)
    if not page:
        return {'bg': '', 'text': '', 'accent': '', 'is_preview': False}
    row = _styles_map().get(page, {})
    return {
        'bg': row.get('bg', ''),
        'text': row.get('text', ''),
        'accent': row.get('accent', ''),
        'is_preview': False,
    }


def build_preview_query(bg: str, text: str, accent: str) -> str:
    params = {'rs_style_preview': '1'}
    if bg:
        params['preview_bg'] = bg
    if text:
        params['preview_text'] = text
    if accent:
        params['preview_accent'] = accent
    return urlencode(params)


# backward compat
def get_page_background_color(request) -> str:
    return get_page_style_vars(request).get('bg', '')
