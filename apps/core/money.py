"""Money helpers: Decimal only, ROUND_HALF_UP to 0.01, never free/negative sales."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TWOPLACES = Decimal('0.01')
MIN_UNIT_PRICE = Decimal('0.01')


def as_decimal(amount) -> Decimal:
    if amount is None or amount == '':
        return Decimal('0')
    if isinstance(amount, Decimal):
        return amount
    try:
        return Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0')


def money(amount) -> Decimal:
    """Round half-up to 2 decimal places."""
    return as_decimal(amount).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def is_sellable_price(amount) -> bool:
    return money(amount) >= MIN_UNIT_PRICE


def require_unit_price(amount) -> Decimal:
    """Return quantized unit price or raise ValueError if not sellable."""
    value = money(amount)
    if value < MIN_UNIT_PRICE:
        raise ValueError('unit price must be at least 0.01')
    return value


def line_total(unit_price, quantity: int) -> Decimal:
    qty = max(0, int(quantity))
    return money(require_unit_price(unit_price) * qty)


def sum_money(amounts) -> Decimal:
    total = Decimal('0')
    for amount in amounts:
        total += money(amount)
    return money(total)


def apply_sale_percents(base_price, percents) -> Decimal:
    """Apply sequential sale percents (акції). Never reaches 0 or negative.

    Example: base 1000, category -20%, product -50% → 400 (not free).
    100% off clamps to MIN_UNIT_PRICE.
    """
    price = money(base_price)
    if price < MIN_UNIT_PRICE:
        raise ValueError('base price must be positive')
    for raw in percents or ():
        pct = as_decimal(raw)
        if pct <= 0:
            continue
        if pct >= 100:
            price = MIN_UNIT_PRICE
            continue
        price = money(price * (Decimal('100') - pct) / Decimal('100'))
        if price < MIN_UNIT_PRICE:
            price = MIN_UNIT_PRICE
    return price


def expected_order_total(order) -> Decimal:
    items_sum = sum_money(row.line_total for row in order.items.all())
    return money(items_sum + money(order.delivery_cost) - money(order.discount))


def reconcile_order_totals(order) -> Decimal:
    """Ensure order.total == items + delivery − discount and total > 0."""
    expected = expected_order_total(order)
    if expected < MIN_UNIT_PRICE:
        raise ValueError('order total must be positive')
    if money(order.total) != expected:
        raise ValueError(
            f'order total mismatch: stored={money(order.total)} expected={expected}'
        )
    return expected
