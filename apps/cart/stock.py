"""Stock availability + soft reservations while items are in a cart."""

from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.cart.models import CartReservation
from apps.catalog.models import Product


def reservation_ttl() -> timedelta:
    return timedelta(seconds=int(getattr(settings, 'SESSION_COOKIE_AGE', 60 * 60 * 24 * 30)))


def purge_expired() -> int:
    deleted, _ = CartReservation.objects.filter(expires_at__lte=timezone.now()).delete()
    return deleted


def reserved_quantity(product_id: int, *, exclude_session_key: str = '', exclude_user_id: int | None = None) -> int:
    purge_expired()
    qs = CartReservation.objects.filter(product_id=product_id, expires_at__gt=timezone.now())
    if exclude_session_key:
        qs = qs.exclude(session_key=exclude_session_key)
    if exclude_user_id:
        qs = qs.exclude(user_id=exclude_user_id)
    return int(qs.aggregate(total=Sum('quantity'))['total'] or 0)


def allocatable(product: Product, *, session_key: str = '', user_id: int | None = None) -> int:
    """Units this holder may keep (physical stock minus others' reservations)."""
    others = reserved_quantity(
        product.id,
        exclude_session_key=session_key or '',
        exclude_user_id=user_id,
    )
    return max(0, int(product.stock) - others)


def free_stock(product_id: int) -> int:
    product = Product.objects.filter(pk=product_id).only('stock').first()
    if not product:
        return 0
    return max(0, int(product.stock) - reserved_quantity(product_id))


def ensure_session_key(session) -> str:
    if not session.session_key:
        session.save()
    return session.session_key or ''


def _expires_at():
    return timezone.now() + reservation_ttl()


@transaction.atomic
def set_reservation(
    product_id: int,
    quantity: int,
    *,
    session_key: str = '',
    user=None,
) -> None:
    purge_expired()
    qty = max(0, int(quantity))
    user_id = getattr(user, 'id', None) if user is not None else None

    if user_id:
        existing = CartReservation.objects.filter(product_id=product_id, user_id=user_id).first()
    elif session_key:
        existing = CartReservation.objects.filter(
            product_id=product_id,
            session_key=session_key,
            user__isnull=True,
        ).first()
    else:
        return

    if qty <= 0:
        if existing:
            existing.delete()
        return

    if existing:
        existing.quantity = qty
        existing.expires_at = _expires_at()
        if session_key and not existing.session_key:
            existing.session_key = session_key
        existing.save(update_fields=['quantity', 'expires_at', 'session_key', 'updated_at'])
        return

    CartReservation.objects.create(
        product_id=product_id,
        quantity=qty,
        session_key=session_key or '',
        user_id=user_id,
        expires_at=_expires_at(),
    )


def release_holder(*, session_key: str = '', user=None) -> None:
    user_id = getattr(user, 'id', None) if user is not None else None
    if user_id:
        CartReservation.objects.filter(user_id=user_id).delete()
    if session_key:
        CartReservation.objects.filter(session_key=session_key, user__isnull=True).delete()


def release_product_for_holder(product_id: int, *, session_key: str = '', user=None) -> None:
    set_reservation(product_id, 0, session_key=session_key, user=user)


def sync_session_reservations(session, lines: list[dict]) -> None:
    sk = ensure_session_key(session)
    wanted = {int(line['product'].id): int(line['quantity']) for line in lines}
    existing = CartReservation.objects.filter(session_key=sk, user__isnull=True)
    for row in existing:
        if row.product_id not in wanted:
            row.delete()
    for product_id, qty in wanted.items():
        set_reservation(product_id, qty, session_key=sk)


def sync_user_reservations(user, lines: list[dict]) -> None:
    wanted = {int(line['product'].id): int(line['quantity']) for line in lines}
    existing = CartReservation.objects.filter(user=user)
    for row in existing:
        if row.product_id not in wanted:
            row.delete()
    for product_id, qty in wanted.items():
        set_reservation(product_id, qty, user=user)


def transfer_session_reservations_to_user(session, user) -> None:
    sk = session.session_key or ''
    if not sk:
        return
    CartReservation.objects.filter(session_key=sk, user__isnull=True).delete()


@transaction.atomic
def consume_for_checkout(items: list[dict], *, session=None, user=None) -> list[str]:
    """Lock rows, ensure stock, decrement, release reservations. Returns issues if blocked."""
    issues: list[str] = []
    locked: list[tuple[Product, int]] = []
    for item in items:
        product = (
            Product.objects.select_for_update()
            .filter(pk=item['product'].id)
            .first()
        )
        qty = int(item['quantity'])
        if product is None or not product.is_active:
            issues.append(_('«%(name)s» більше недоступний') % {
                'name': getattr(item.get('product'), 'name', '—'),
            })
            continue
        if product.stock < qty:
            if product.stock <= 0:
                issues.append(_('«%(name)s» закінчився на складі') % {'name': product.name})
            else:
                issues.append(
                    _('«%(name)s»: на складі лише %(n)s шт.') % {
                        'name': product.name,
                        'n': product.stock,
                    }
                )
            continue
        locked.append((product, qty))

    if issues:
        return issues

    for product, qty in locked:
        product.stock = int(product.stock) - qty
        product.save(update_fields=['stock'])

    sk = ''
    if session is not None:
        sk = session.session_key or ''
    release_holder(session_key=sk, user=user if getattr(user, 'is_authenticated', False) else None)
    return []


def availability_issues(items: list[dict]) -> list[str]:
    """Read-only checks for checkout / cart hints (live stock, no price snapshot)."""
    issues: list[str] = []
    for item in items:
        product = item['product']
        qty = int(item['quantity'])
        if item.get('is_missing') or getattr(product, '_missing', False):
            issues.append(_('«%(name)s» більше недоступний') % {
                'name': getattr(product, 'name', _('Товар недоступний')),
            })
            continue
        if not getattr(product, 'is_active', True):
            issues.append(_('«%(name)s» більше недоступний') % {'name': product.name})
            continue
        # Brand/category soft-off also block storefront purchases
        brand = getattr(product, 'brand', None)
        category = getattr(product, 'category', None)
        if brand is not None and hasattr(brand, 'is_active') and not brand.is_active:
            issues.append(_('«%(name)s» більше недоступний') % {'name': product.name})
            continue
        if category is not None and hasattr(category, 'is_active') and not category.is_active:
            issues.append(_('«%(name)s» більше недоступний') % {'name': product.name})
            continue
        stock = int(product.stock)
        if stock <= 0:
            issues.append(_('«%(name)s» закінчився на складі') % {'name': product.name})
        elif stock < qty:
            issues.append(
                _('«%(name)s»: на складі лише %(n)s шт.') % {
                    'name': product.name,
                    'n': stock,
                }
            )
        from apps.core.money import is_sellable_price
        if not is_sellable_price(getattr(product, 'base_price', 0)):
            issues.append(_('«%(name)s» недоступний для замовлення (некоректна ціна)') % {
                'name': product.name,
            })
    return issues
