"""Cart line quantity parsing and hard limits."""

from __future__ import annotations

MAX_LINE_QTY = 99


def parse_product_id(raw) -> int:
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError, AttributeError):
        return 0
    return value if value > 0 else 0


def parse_quantity(raw, *, default: int = 1) -> int:
    """Strict int parse: floats/text → default; negatives kept for update/remove."""
    if raw is None:
        return default
    text = str(raw).strip()
    if not text:
        return default
    if '.' in text or ',' in text or 'e' in text.lower() or 'E' in text:
        return default
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


def clamp_line_qty(quantity: int, *, stock_cap: int) -> int:
    """Positive line qty capped by stock and MAX_LINE_QTY."""
    qty = int(quantity)
    if qty <= 0:
        return 0
    cap = min(MAX_LINE_QTY, max(0, int(stock_cap)))
    return min(qty, cap)
