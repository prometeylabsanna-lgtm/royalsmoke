from __future__ import annotations

from django.core.cache import cache

from apps.core.models import PageStyle, SiteBlock, clear_site_content_cache

PAGE_STYLES_CACHE_KEY = 'page_styles'

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


def ensure_page_styles() -> int:
    """Ідемпотентне створення записів PageStyle для всіх сторінок."""
    created = 0
    for value, _label in SiteBlock.Page.choices:
        _, was_created = PageStyle.objects.get_or_create(
            page=value,
            defaults={'background_color': ''},
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


def _styles_map() -> dict[str, str]:
    cached = cache.get(PAGE_STYLES_CACHE_KEY)
    if cached is not None:
        return cached
    data = {
        row.page: (row.background_color or '').strip()
        for row in PageStyle.objects.all()
    }
    cache.set(PAGE_STYLES_CACHE_KEY, data, 300)
    return data


def get_page_background_color(request) -> str:
    """Кастомний HEX або порожній рядок (дефолт CSS)."""
    page = resolve_page_key(request)
    if not page:
        return ''
    return _styles_map().get(page, '')
