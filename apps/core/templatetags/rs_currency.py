from __future__ import annotations

from django import template

from apps.core.currency import convert_from_uah, get_currency

register = template.Library()


@register.filter
def money(amount):
    """Convert a UAH amount into the active language currency."""
    return convert_from_uah(amount)


@register.filter
def currency_symbol(code=None):
    return get_currency(code)['symbol']
