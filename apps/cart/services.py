from __future__ import annotations

from decimal import Decimal

from django.shortcuts import get_object_or_404

from apps.catalog.models import Product, ProductVariant

CART_SESSION_KEY = 'rs_cart'


def _cart(session) -> dict:
    cart = session.get(CART_SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[CART_SESSION_KEY] = cart
    return cart


def _line_key(product_id: int, variant_id: int | None) -> str:
    return f'{product_id}:{variant_id or 0}'


def add_item(session, product_id: int, quantity: int = 1, variant_id: int | None = None) -> dict:
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, pk=variant_id, product=product, is_active=True)
    key = _line_key(product.id, variant.id if variant else None)
    cart = _cart(session)
    line = cart.get(key, {'product_id': product.id, 'variant_id': variant.id if variant else None, 'qty': 0})
    line['qty'] = int(line.get('qty', 0)) + max(1, int(quantity))
    cart[key] = line
    session.modified = True
    return cart


def set_quantity(session, product_id: int, quantity: int, variant_id: int | None = None) -> dict:
    key = _line_key(product_id, variant_id)
    cart = _cart(session)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        if key not in cart:
            return add_item(session, product_id, quantity, variant_id)
        cart[key]['qty'] = int(quantity)
    session.modified = True
    return cart


def remove_item(session, product_id: int, variant_id: int | None = None) -> dict:
    cart = _cart(session)
    cart.pop(_line_key(product_id, variant_id), None)
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
        for p in Product.objects.filter(id__in=product_ids).select_related('brand').prefetch_related('variants', 'images')
    }
    items = []
    for key, raw in cart.items():
        product = products.get(int(raw['product_id']))
        if not product:
            continue
        variant = None
        vid = raw.get('variant_id')
        if vid:
            variant = next((v for v in product.variants.all() if v.id == int(vid)), None)
        price = variant.price if variant else product.base_price
        qty = int(raw.get('qty', 1))
        items.append({
            'key': key,
            'product': product,
            'variant': variant,
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
