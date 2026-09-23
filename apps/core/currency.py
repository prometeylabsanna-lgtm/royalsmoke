"""Language-bound storefront currency: convert from UAH using admin rates.

Add a language in settings.LANGUAGE_CURRENCY and a CurrencyRate row in admin.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.cache import cache
from django.db.utils import OperationalError, ProgrammingError
from django.utils.translation import get_language

from apps.core.money import TWOPLACES, as_decimal, money

CACHE_KEY = 'rs_currency_rates'

_FALLBACK: dict[str, dict] = {
    'UAH': {
        'code': 'UAH',
        'symbol': '₴',
        'name': 'Гривня',
        'uah_per_unit': Decimal('1'),
    },
    'USD': {
        'code': 'USD',
        'symbol': '$',
        'name': 'Долар США',
        'uah_per_unit': Decimal('41.00'),
    },
    'CNY': {
        'code': 'CNY',
        'symbol': '¥',
        'name': 'Юань',
        'uah_per_unit': Decimal('5.80'),
    },
}


def clear_currency_cache() -> None:
    cache.delete(CACHE_KEY)


def language_currency_code(lang: str | None = None) -> str:
    raw = (lang or get_language() or getattr(settings, 'LANGUAGE_CODE', 'uk') or 'uk')
    lang = str(raw).lower()
    mapping = getattr(settings, 'LANGUAGE_CURRENCY', {}) or {}
    if lang in mapping:
        return str(mapping[lang]).upper()
    base = lang.split('-', 1)[0]
    if base in mapping:
        return str(mapping[base]).upper()
    return str(
        mapping.get('uk') or getattr(settings, 'CURRENCY_CODE', 'UAH') or 'UAH'
    ).upper()


def get_rates() -> dict[str, dict]:
    cached = cache.get(CACHE_KEY)
    if isinstance(cached, dict) and cached:
        return cached
    rates = {code: dict(row) for code, row in _FALLBACK.items()}
    try:
        from apps.core.models import CurrencyRate

        for row in CurrencyRate.objects.all():
            rate = as_decimal(row.uah_per_unit)
            if rate <= 0:
                rate = Decimal('1')
            rates[row.code.upper()] = {
                'code': row.code.upper(),
                'symbol': row.symbol or rates.get(row.code.upper(), {}).get('symbol', row.code),
                'name': row.name or row.code,
                'uah_per_unit': rate,
            }
    except (OperationalError, ProgrammingError):
        pass
    cache.set(CACHE_KEY, rates, 300)
    return rates


def get_currency(code: str | None = None) -> dict:
    resolved = (code or language_currency_code() or 'UAH').upper()
    rates = get_rates()
    return rates.get(resolved) or rates.get('UAH') or _FALLBACK['UAH']


def convert_from_uah(amount, code: str | None = None) -> Decimal:
    value = as_decimal(amount)
    cur = get_currency(code)
    rate = as_decimal(cur.get('uah_per_unit'))
    if cur.get('code') == 'UAH' or rate <= 0:
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return (value / rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def convert_to_uah(amount, code: str | None = None) -> Decimal:
    value = as_decimal(amount)
    cur = get_currency(code)
    rate = as_decimal(cur.get('uah_per_unit'))
    if cur.get('code') == 'UAH' or rate <= 0:
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return (value * rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def convert_from_uah_int(amount, code: str | None = None) -> int:
    value = convert_from_uah(amount, code)
    return int(value.to_integral_value(rounding=ROUND_HALF_UP))


def amount_to_uah(amount, *, currency: str | None = None, fx_rate=None) -> Decimal:
    """Convert a stored order amount back to UAH using the snapshot rate."""
    value = as_decimal(amount)
    code = (currency or 'UAH').upper()
    if code == 'UAH':
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    rate = as_decimal(fx_rate)
    if rate <= 0:
        rate = as_decimal(get_currency(code).get('uah_per_unit'))
    if rate <= 0:
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return (value * rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def convert_cart_totals(totals: dict, delivery_uah=None) -> dict:
    """Return cart-like totals converted from UAH into the active currency."""
    cur = get_currency()
    items = []
    for item in totals.get('items') or []:
        unit = convert_from_uah(item.get('unit_price'))
        qty = int(item.get('quantity') or 0)
        line = money(unit * qty)
        items.append({**item, 'unit_price': unit, 'line_total': line})
    subtotal = money(sum((i['line_total'] for i in items), Decimal('0')))
    delivery = convert_from_uah(delivery_uah or 0)
    discount = money((totals.get('discount') if totals else None) or 0)
    total = money(subtotal + delivery - discount)
    return {
        **totals,
        'items': items,
        'subtotal': subtotal,
        'delivery_cost': delivery,
        'discount': discount,
        'total': total,
        'currency': cur['code'],
        'fx_rate': cur['uah_per_unit'],
        'symbol': cur['symbol'],
    }
