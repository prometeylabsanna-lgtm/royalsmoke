from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.catalog.models import Product

COMPARE_SESSION_KEY = 'rs_compare'
COMPARE_MAX = 4


def _session_ids(session) -> list[int]:
    raw = session.get(COMPARE_SESSION_KEY)
    if not isinstance(raw, list):
        return []
    out: list[int] = []
    seen: set[int] = set()
    for item in raw:
        try:
            pid = int(item)
        except (TypeError, ValueError):
            continue
        if pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


def _set_session_ids(session, ids: list[int]) -> None:
    seen: set[int] = set()
    out: list[int] = []
    for pid in ids:
        if pid not in seen:
            seen.add(pid)
            out.append(int(pid))
    session[COMPARE_SESSION_KEY] = out[:COMPARE_MAX]
    session.modified = True


def product_ids(request) -> set[int]:
    return set(_session_ids(request.session))


def ordered_ids(request) -> list[int]:
    return _session_ids(request.session)


def count(request) -> int:
    return len(ordered_ids(request))


def contains(request, product_id: int) -> bool:
    return int(product_id) in product_ids(request)


def toggle(request, product_id: int) -> bool:
    """Toggle product. Returns True if it is now in compare. Caps at COMPARE_MAX."""
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    ids = _session_ids(request.session)
    if product.id in ids:
        _set_session_ids(request.session, [i for i in ids if i != product.id])
        return False
    if len(ids) >= COMPARE_MAX:
        ids = ids[-(COMPARE_MAX - 1) :]
    ids.append(product.id)
    _set_session_ids(request.session, ids)
    return True


def remove(request, product_id: int) -> None:
    pid = int(product_id)
    ids = [i for i in _session_ids(request.session) if i != pid]
    _set_session_ids(request.session, ids)


def clear(request) -> None:
    _set_session_ids(request.session, [])


def items(request) -> list[Product]:
    ids = ordered_ids(request)
    if not ids:
        return []
    products = {
        p.id: p
        for p in Product.objects.on_storefront()
        .filter(id__in=ids)
        .select_related('brand', 'line', 'category')
        .prefetch_related('variants', 'images')
    }
    return [products[i] for i in ids if i in products]
