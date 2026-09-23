"""DB-backed cart for authenticated API clients + merge from session."""

from __future__ import annotations

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.cart import services as session_cart
from apps.cart import stock as stock_svc
from apps.cart.models import Cart, CartItem
from apps.cart.qty import clamp_line_qty
from apps.catalog.models import Product


def get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def _db_lines(cart: Cart) -> list[dict]:
    rows = cart.items.select_related('product', 'product__brand').prefetch_related('product__images')
    return [
        {
            'id': row.id,
            'key': str(row.product_id),
            'product': row.product,
            'quantity': row.quantity,
            'unit_price': row.product.base_price,
            'line_total': row.product.base_price * row.quantity,
        }
        for row in rows
    ]


def load_user_cart_into_session(session, user) -> None:
    cart = get_or_create_cart(user)
    lines = _db_lines(cart)
    session_cart.replace_raw(
        session,
        [{'product_id': line['product'].id, 'qty': line['quantity']} for line in lines],
    )
    sk = session.session_key or ''
    if sk:
        stock_svc.release_holder(session_key=sk)
    stock_svc.sync_user_reservations(user, lines)


def merge_session_into_user(session, user) -> Cart:
    """Merge guest session into profile cart: max(guest, user), capped by stock.

    Profile is source of truth after merge; session is rebuilt from DB.
    """
    cart = get_or_create_cart(user)
    sk = session.session_key or ''
    session_items = session_cart.cart_items(session)
    with transaction.atomic():
        guest_by_product = {item['product'].id: item['quantity'] for item in session_items}
        product_ids = set(guest_by_product)
        product_ids.update(cart.items.values_list('product_id', flat=True))
        products = {
            p.id: p
            for p in Product.objects.filter(id__in=product_ids).select_for_update()
        }
        for product_id in product_ids:
            product = products.get(product_id)
            if product is None or not product.is_active:
                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
                continue
            existing = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            user_qty = existing.quantity if existing else 0
            guest_qty = guest_by_product.get(product_id, 0)
            qty = min(
                max(guest_qty, user_qty),
                stock_svc.allocatable(product, session_key=sk, user_id=user.id),
            )
            if qty <= 0:
                if existing:
                    existing.delete()
                continue
            if existing:
                if existing.quantity != qty:
                    existing.quantity = qty
                    existing.save(update_fields=['quantity'])
            else:
                CartItem.objects.create(cart=cart, product=product, quantity=qty)

        stock_svc.transfer_session_reservations_to_user(session, user)
        session_cart.clear(session)
        lines = _db_lines(cart)
        stock_svc.sync_user_reservations(user, lines)
        load_user_cart_into_session(session, user)
    return cart


def replace_from_session(session, user) -> Cart:
    """Mirror session cart into DB (web dual-write for authenticated users)."""
    cart = get_or_create_cart(user)
    items = session_cart.cart_items(session)
    with transaction.atomic():
        keep_ids: set[int] = set()
        for item in items:
            product = item['product']
            cap = stock_svc.allocatable(product, user_id=user.id)
            qty = min(int(item['quantity']), cap)
            if qty <= 0:
                continue
            row, _ = CartItem.objects.update_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': qty},
            )
            keep_ids.add(row.id)
        cart.items.exclude(id__in=keep_ids).delete()
        lines = _db_lines(cart)
        stock_svc.sync_user_reservations(user, lines)
        sk = session.session_key or ''
        if sk:
            stock_svc.release_holder(session_key=sk)
    return cart


def add_item(user, product_id: int, quantity: int = 1) -> Cart:
    from apps.core.money import is_sellable_price

    cart = get_or_create_cart(user)
    product = get_object_or_404(Product.objects.on_storefront(), pk=product_id)
    if not is_sellable_price(product.base_price):
        return cart
    item = CartItem.objects.filter(cart=cart, product=product).first()
    current = item.quantity if item else 0
    desired = current + max(1, int(quantity))
    capped = clamp_line_qty(
        desired,
        stock_cap=stock_svc.allocatable(product, user_id=user.id),
    )
    if capped <= 0:
        return cart
    if item:
        item.quantity = capped
        item.save(update_fields=['quantity'])
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=capped)
    stock_svc.set_reservation(product.id, capped, user=user)
    return cart


def set_quantity(user, item_id: int, quantity: int) -> Cart:
    cart = get_or_create_cart(user)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    if quantity <= 0:
        pid = item.product_id
        item.delete()
        stock_svc.release_product_for_holder(pid, user=user)
        return cart
    product = item.product
    capped = clamp_line_qty(
        int(quantity),
        stock_cap=stock_svc.allocatable(product, user_id=user.id),
    )
    if capped <= 0:
        pid = item.product_id
        item.delete()
        stock_svc.release_product_for_holder(pid, user=user)
        return cart
    item.quantity = capped
    item.save(update_fields=['quantity'])
    stock_svc.set_reservation(product.id, capped, user=user)
    return cart


def remove_item(user, item_id: int) -> Cart:
    cart = get_or_create_cart(user)
    item = CartItem.objects.filter(pk=item_id, cart=cart).first()
    if item:
        pid = item.product_id
        item.delete()
        stock_svc.release_product_for_holder(pid, user=user)
    return cart


def clear(user) -> None:
    cart = get_or_create_cart(user)
    cart.items.all().delete()
    stock_svc.release_holder(user=user)


def cart_totals(user) -> dict:
    from apps.core.money import is_sellable_price, line_total as money_line_total
    from apps.core.money import money, sum_money

    cart = get_or_create_cart(user)
    items_qs = list(cart.items.select_related('product', 'product__brand'))
    items = []
    for row in items_qs:
        product = row.product
        qty = row.quantity
        price = money(product.base_price)
        total = money_line_total(price, qty) if is_sellable_price(price) else money(0)
        items.append({
            'id': row.id,
            'key': str(row.product_id),
            'product': product,
            'quantity': qty,
            'unit_price': price,
            'line_total': total,
        })
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
