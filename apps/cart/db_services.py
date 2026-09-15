"""DB-backed cart for authenticated API clients + merge from session."""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart, CartItem
from apps.cart import services as session_cart
from apps.catalog.models import Product, ProductVariant


def get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def merge_session_into_user(session, user) -> Cart:
    cart = get_or_create_cart(user)
    session_items = session_cart.cart_items(session)
    with transaction.atomic():
        for item in session_items:
            product = item['product']
            variant = item['variant']
            existing = CartItem.objects.filter(
                cart=cart, product=product, variant=variant,
            ).first()
            if existing:
                existing.quantity += item['quantity']
                existing.save(update_fields=['quantity'])
            else:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    variant=variant,
                    quantity=item['quantity'],
                )
        session_cart.clear(session)
    return cart


def add_item(user, product_id: int, quantity: int = 1, variant_id: int | None = None) -> Cart:
    cart = get_or_create_cart(user)
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, pk=variant_id, product=product, is_active=True)
    qs = CartItem.objects.filter(cart=cart, product=product)
    if variant:
        qs = qs.filter(variant=variant)
    else:
        qs = qs.filter(variant__isnull=True)
    item = qs.first()
    if item:
        item.quantity += max(1, int(quantity))
        item.save(update_fields=['quantity'])
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            variant=variant,
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
    items_qs = cart.items.select_related('product', 'variant', 'product__brand')
    items = []
    for row in items_qs:
        price = row.variant.price if row.variant_id else row.product.base_price
        qty = row.quantity
        items.append({
            'id': row.id,
            'key': f'{row.product_id}:{row.variant_id or 0}',
            'product': row.product,
            'variant': row.variant,
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
