from __future__ import annotations

from decimal import Decimal

from django.shortcuts import get_object_or_404

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
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    key = _line_key(product.id)
    cart = _cart(session)
    line = cart.get(key, {'product_id': product.id, 'qty': 0})
    line['qty'] = int(line.get('qty', 0)) + max(1, int(quantity))
    cart[key] = line
    session.modified = True
    return cart


def set_quantity(session, product_id: int, quantity: int) -> dict:
    key = _line_key(product_id)
    cart = _cart(session)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        if key not in cart:
            return add_item(session, product_id, quantity)
        cart[key]['qty'] = int(quantity)
    session.modified = True
    return cart


def remove_item(session, product_id: int) -> dict:
    cart = _cart(session)
    cart.pop(_line_key(product_id), None)
    session.modified = True
    return cart


def clear(session) -> None:
    session[CART_SESSION_KEY] = {}
    session.modified = True


def cart_items(session) -> list[dict]:
    cart = _cart(session)
    if not cart:
        return []
    product_ids = {int(v['product_id']) for v in cart.values()}
    products = {
        p.id: p
        for p in Product.objects.filter(id__in=product_ids).select_related('brand').prefetch_related('images')
    }
    items = []
    for key, raw in cart.items():
        product = products.get(int(raw['product_id']))
        if not product:
            continue
        price = product.base_price
        qty = int(raw.get('qty', 1))
        items.append({
            'key': key,
            'product': product,
            'quantity': qty,
            'unit_price': price,
            'line_total': price * qty,
        })
    return items


def cart_totals(session) -> dict:
    items = cart_items(session)
    subtotal = sum((i['line_total'] for i in items), Decimal('0'))
    count = sum(i['quantity'] for i in items)
    return {
        'items': items,
        'subtotal': subtotal,
        'count': count,
        'total': subtotal,
    }
