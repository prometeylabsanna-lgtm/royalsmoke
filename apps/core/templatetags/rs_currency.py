from __future__ import annotations

from django import template
from django.utils import numberformat
from django.utils.formats import get_format

from apps.core.currency import ZERO_DECIMAL_CURRENCIES, convert_from_uah, get_currency

register = template.Library()


@register.filter
def money(amount):
    """Convert a UAH amount into the active language currency.

    Для IDR/VND повертає цілу суму з групами розрядів за мовою сторінки (910.256),
    для решти валют — Decimal з двома знаками, як і раніше.
    """
    value = convert_from_uah(amount)
    if get_currency()['code'] in ZERO_DECIMAL_CURRENCIES:
        # Групи по 3 розряди явно: у форматах id/vi NUMBER_GROUPING не задано.
        return numberformat.format(
            value,
            get_format('DECIMAL_SEPARATOR'),
            decimal_pos=0,
            grouping=3,
            thousand_sep=get_format('THOUSAND_SEPARATOR'),
            force_grouping=True,
        )
    return value


@register.filter
def currency_symbol(code=None):
    return get_currency(code)['symbol']
