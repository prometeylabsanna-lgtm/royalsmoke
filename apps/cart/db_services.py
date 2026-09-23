"""DB-backed cart for authenticated API clients + merge from session."""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart, CartItem
from apps.cart import services as session_cart
from apps.catalog.models import Product


def get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def merge_session_into_user(session, user) -> Cart:
    cart = get_or_create_cart(user)
    session_items = session_cart.cart_items(session)
    with transaction.atomic():
        for item in session_items:
            product = item['product']
            existing = CartItem.objects.filter(cart=cart, product=product).first()
            if existing:
                existing.quantity += item['quantity']
                existing.save(update_fields=['quantity'])
            else:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=item['quantity'],
                )
        session_cart.clear(session)
    return cart


def add_item(user, product_id: int, quantity: int = 1) -> Cart:
    cart = get_or_create_cart(user)
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    item = CartItem.objects.filter(cart=cart, product=product).first()
    if item:
        item.quantity += max(1, int(quantity))
        item.save(update_fields=['quantity'])
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=max(1, int(quantity)),
        )
    return cart


def set_quantity(user, item_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(user)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = int(quantity)
        item.save(update_fields=['quantity'])
    return cart


def remove_item(user, item_id: int) -> Cart:
    cart = get_or_create_cart(user)
    CartItem.objects.filter(pk=item_id, cart=cart).delete()
    return cart


def clear(user) -> None:
    cart = get_or_create_cart(user)
    cart.items.all().delete()


def cart_totals(user) -> dict:
    cart = get_or_create_cart(user)
    items_qs = cart.items.select_related('product', 'product__brand')
    items = []
    for row in items_qs:
        price = row.product.base_price
        qty = row.quantity
        items.append({
            'id': row.id,
            'key': str(row.product_id),
            'product': row.product,
            'quantity': qty,
            'unit_price': price,
            'line_total': price * qty,
        })
    subtotal = sum((i['line_total'] for i in items), Decimal('0'))
    count = sum(i['quantity'] for i in items)
    return {
        'items': items,
        'subtotal': subtotal,
        'count': count,
        'total': subtotal,
    }
