"""Фіксований набір юридичних сторінок (CMS як Доставка)."""

from __future__ import annotations

# URL slug → SiteBlock.Page value (age_policy ≠ age gate)
LEGAL_SLUG_TO_PAGE: dict[str, str] = {
    'privacy': 'privacy',
    'terms': 'terms',
    'age': 'age_policy',
    'cookies': 'cookies',
}

LEGAL_PAGE_TO_SLUG: dict[str, str] = {v: k for k, v in LEGAL_SLUG_TO_PAGE.items()}

LEGAL_NAV_ORDER: tuple[str, ...] = ('privacy', 'terms', 'age', 'cookies')


def legal_page_key(slug: str) -> str | None:
    return LEGAL_SLUG_TO_PAGE.get(slug)
