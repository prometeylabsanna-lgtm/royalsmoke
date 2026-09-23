from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.accounts.models import WishlistItem
from apps.catalog.models import Product

WISHLIST_SESSION_KEY = 'rs_wishlist'


def _session_ids(session) -> list[int]:
    raw = session.get(WISHLIST_SESSION_KEY)
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
    session[WISHLIST_SESSION_KEY] = out
    session.modified = True


def _db_ids(user) -> list[int]:
    return list(
        WishlistItem.objects.filter(user=user)
        .order_by('-created_at')
        .values_list('product_id', flat=True)
    )


def product_ids(request) -> set[int]:
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return set(_db_ids(user))
    return set(_session_ids(request.session))


def ordered_ids(request) -> list[int]:
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return _db_ids(user)
    return _session_ids(request.session)


def count(request) -> int:
    return len(ordered_ids(request))


def toggle(request, product_id: int) -> bool:
    """Toggle product. Returns True if it is now in the wishlist."""
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    user = request.user

    if user.is_authenticated:
        item, created = WishlistItem.objects.get_or_create(user=user, product=product)
        if not created:
            item.delete()
            ids = [i for i in _session_ids(request.session) if i != product.id]
            _set_session_ids(request.session, ids)
            return False
        ids = _session_ids(request.session)
        if product.id not in ids:
            ids.insert(0, product.id)
            _set_session_ids(request.session, ids)
        return True

    ids = _session_ids(request.session)
    if product.id in ids:
        ids = [i for i in ids if i != product.id]
        _set_session_ids(request.session, ids)
        return False
    ids.insert(0, product.id)
    _set_session_ids(request.session, ids)
    return True


def items(request) -> list[Product]:
    ids = ordered_ids(request)
    if not ids:
        return []
    products = {
        p.id: p
        for p in Product.objects.on_storefront()
        .filter(id__in=ids)
        .select_related('brand', 'line')
        .prefetch_related('images')
    }
    return [products[i] for i in ids if i in products]


def merge_session_to_user(request) -> None:
    """On login/register: push session wishlist into DB, then sync session from DB."""
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated:
        return
    session_ids = _session_ids(request.session)
    if session_ids:
        valid = set(
            Product.objects.on_storefront()
            .filter(id__in=session_ids)
            .values_list('id', flat=True)
        )
        for pid in session_ids:
            if pid in valid:
                WishlistItem.objects.get_or_create(user=user, product_id=pid)
    _set_session_ids(request.session, _db_ids(user))
