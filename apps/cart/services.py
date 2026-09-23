from __future__ import annotations

from django.shortcuts import get_object_or_404

from apps.cart import stock as stock_svc
from apps.cart.qty import MAX_LINE_QTY, clamp_line_qty
from apps.cart.stubs import MissingProduct
from apps.catalog.models import Product

CART_SESSION_KEY = 'rs_cart'


def _cart(session) -> dict:
    cart = session.get(CART_SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def _line_key(product_id: int) -> str:
    return str(product_id)


def add_item(session, product_id: int, quantity: int = 1) -> dict:
    from apps.core.money import is_sellable_price

    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    if not is_sellable_price(product.base_price):
        return _cart(session)
    sk = stock_svc.ensure_session_key(session)
    key = _line_key(product.id)
    cart = _cart(session)
    current = int(cart.get(key, {}).get('qty', 0))
    desired = current + max(1, int(quantity))
    capped = clamp_line_qty(
        desired,
        stock_cap=stock_svc.allocatable(product, session_key=sk),
    )
    if capped <= 0:
        return cart
    cart[key] = {'product_id': product.id, 'qty': capped}
    session.modified = True
    stock_svc.set_reservation(product.id, capped, session_key=sk)
    return cart


def set_quantity(session, product_id: int, quantity: int) -> dict:
    """Last-write-wins set. Missing/inactive SKUs: silently no-op on invalid add-back."""
    key = _line_key(product_id)
    cart = _cart(session)
    sk = stock_svc.ensure_session_key(session)
    if quantity <= 0:
        cart.pop(key, None)
        session.modified = True
        stock_svc.release_product_for_holder(product_id, session_key=sk)
        return cart

    product = Product.objects.filter(pk=product_id).first()
    if product is None:
        # Deleted SKU still in cart: keep row, ignore qty mutation beyond remove.
        if key not in cart:
            return cart
        cart[key]['qty'] = min(MAX_LINE_QTY, max(1, int(quantity)))
        session.modified = True
        return cart

    capped = clamp_line_qty(
        int(quantity),
        stock_cap=stock_svc.allocatable(product, session_key=sk),
    )
    if capped <= 0:
        cart.pop(key, None)
        session.modified = True
        stock_svc.release_product_for_holder(product_id, session_key=sk)
        return cart
    cart[key] = {'product_id': product.id, 'qty': capped}
    session.modified = True
    stock_svc.set_reservation(product.id, capped, session_key=sk)
    return cart


def remove_item(session, product_id: int) -> dict:
    cart = _cart(session)
    cart.pop(_line_key(product_id), None)
    session.modified = True
    sk = session.session_key or ''
    if sk:
        stock_svc.release_product_for_holder(product_id, session_key=sk)
    return cart


def clear(session) -> None:
    sk = session.session_key or ''
    session[CART_SESSION_KEY] = {}
    session.modified = True
    if sk:
        stock_svc.release_holder(session_key=sk)


def replace_raw(session, lines: list[dict]) -> None:
    """Overwrite session cart from [{product_id, qty}, ...] and sync reservations."""
    cart: dict = {}
    for line in lines:
        pid = int(line['product_id'])
        qty = int(line['qty'])
        if qty > 0:
            cart[_line_key(pid)] = {'product_id': pid, 'qty': qty}
    session[CART_SESSION_KEY] = cart
    session.modified = True
    stock_svc.sync_session_reservations(session, cart_items(session))


def cart_items(session) -> list[dict]:
    from apps.core.money import is_sellable_price, line_total as money_line_total
    from apps.core.money import money

    cart = _cart(session)
    if not cart:
        return []
    product_ids = {int(v['product_id']) for v in cart.values()}
    products = {
        p.id: p
        for p in Product.objects.filter(id__in=product_ids).select_related(
            'brand', 'category',
        ).prefetch_related('images')
    }
    items = []
    for key, raw in cart.items():
        pid = int(raw['product_id'])
        product = products.get(pid) or MissingProduct(pid)
        qty = max(1, int(raw.get('qty', 1)))
        price = money(product.base_price)
        total = money_line_total(price, qty) if is_sellable_price(price) else money(0)
        items.append({
            'key': key,
            'product': product,
            'quantity': qty,
            'unit_price': price,
            'line_total': total,
            'is_missing': bool(getattr(product, '_missing', False)),
        })
    return items


def cart_totals(session) -> dict:
    from apps.core.money import sum_money

    items = cart_items(session)
    subtotal = sum_money(i['line_total'] for i in items)
    count = sum(i['quantity'] for i in items)
    issues = stock_svc.availability_issues(items)
    return {
        'items': items,
        'subtotal': subtotal,
        'count': count,
        'total': subtotal,
        'issues': issues,
        'can_checkout': not issues and bool(items),
    }
