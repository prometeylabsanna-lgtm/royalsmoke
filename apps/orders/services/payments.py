"""Payment settlement shared by LiqPay callbacks and demo checkout."""

from __future__ import annotations

from django.conf import settings
from django.db import transaction
from django.urls import reverse

from apps.orders.models import Order, Payment
from apps.orders.services import liqpay as liqpay_svc
from apps.orders.services import notify_order_paid

_PAID_STATUSES = frozenset({'success', 'sandbox', 'wait_accept'})
_FAIL_STATUSES = frozenset({'failure', 'error', 'reversed'})


def demo_payments_enabled() -> bool:
    return bool(getattr(settings, 'DEMO_PAYMENTS', False))


def ensure_pending_payment(order: Order, *, provider: str | None = None) -> Payment:
    from apps.core.money import money, reconcile_order_totals

    reconcile_order_totals(order)
    defaults = {
        'order': order,
        'amount': money(order.total),
        'currency': order.currency,
        'status': Payment.STATUS_PENDING,
    }
    if provider:
        defaults['provider'] = provider
    payment, created = Payment.objects.get_or_create(
        liqpay_order_id=order.order_number,
        defaults=defaults,
    )
    if not created and provider and payment.provider != provider:
        payment.provider = provider
        payment.save(update_fields=['provider', 'updated_at'])
    return payment


def settle_payment(
    order: Order,
    *,
    status: str,
    payload: dict | None = None,
    provider: str | None = None,
    transaction_id: str = '',
) -> bool:
    """Apply a payment result. Returns True if the order was newly marked paid."""
    status = (status or '').lower()
    payload = payload or {}
    paid_now = False
    with transaction.atomic():
        locked = Order.objects.select_for_update().get(pk=order.pk)
        payment, _ = Payment.objects.select_for_update().get_or_create(
            liqpay_order_id=locked.order_number,
            defaults={
                'order': locked,
                'amount': locked.total,
                'currency': locked.currency,
                'status': Payment.STATUS_PENDING,
            },
        )
        if provider:
            payment.provider = provider
        if payment.status == Payment.STATUS_SUCCESS and locked.status == Order.STATUS_PAID:
            return False
        payment.raw_callback = payload
        if transaction_id:
            payment.transaction_id = str(transaction_id)
        if status in _PAID_STATUSES:
            payment.status = Payment.STATUS_SUCCESS
            locked.status = Order.STATUS_PAID
            locked.save(update_fields=['status', 'updated_at'])
            payment.save()
            paid_now = True
        elif status in _FAIL_STATUSES:
            payment.status = (
                Payment.STATUS_REVERSED if status == 'reversed' else Payment.STATUS_FAILURE
            )
            payment.save()
        else:
            payment.status = Payment.STATUS_PENDING
            payment.save()
        if paid_now:
            order_pk = locked.pk
            transaction.on_commit(
                lambda: notify_order_paid(Order.objects.get(pk=order_pk))
            )
    return paid_now


def online_payment_payload(request, order: Order) -> dict:
    """Extra checkout payload for API clients."""
    if demo_payments_enabled():
        ensure_pending_payment(order, provider=Payment.PROVIDER_DEMO)
        return {
            'demo': True,
            'demo_pay_url': request.build_absolute_uri(
                reverse('orders:pay', kwargs={'order_number': order.order_number})
            ),
            'liqpay': None,
        }
    try:
        liq = liqpay_svc.create_checkout_payload(
            order,
            result_url=request.build_absolute_uri(
                reverse('orders_liqpay_result') + f'?order={order.order_number}'
            ),
            server_url=request.build_absolute_uri(reverse('orders_liqpay_callback')),
        )
    except ValueError:
        return {'demo': False, 'demo_pay_url': None, 'liqpay': None}
    ensure_pending_payment(order, provider=Payment.PROVIDER_LIQPAY)
    return {
        'demo': False,
        'demo_pay_url': None,
        'liqpay': {
            'data': liq['data'],
            'signature': liq['signature'],
            'checkout_url': liq['checkout_url'],
        },
    }
