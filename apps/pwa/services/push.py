from __future__ import annotations

import json
import logging
from typing import Iterable

from django.conf import settings
from django.db.models import Q
from django.utils.translation import activate, get_language, gettext as _

from apps.pwa.models import PushSubscription

logger = logging.getLogger(__name__)


def vapid_configured() -> bool:
    return bool(
        getattr(settings, 'VAPID_PRIVATE_KEY', '')
        and getattr(settings, 'VAPID_PUBLIC_KEY', '')
    )


def vapid_public_key() -> str:
    return getattr(settings, 'VAPID_PUBLIC_KEY', '') or ''


def _vapid_claims() -> dict:
    email = (getattr(settings, 'VAPID_ADMIN_EMAIL', '') or settings.DEFAULT_FROM_EMAIL or '').strip()
    if email and not email.startswith('mailto:'):
        email = f'mailto:{email}'
    return {'sub': email or 'mailto:admin@localhost'}


def send_web_push(subscription: PushSubscription, payload: dict) -> bool:
    if not vapid_configured() or not subscription.is_active:
        return False
    try:
        from pywebpush import WebPushException, webpush
    except ImportError:
        logger.warning('pywebpush is not installed')
        return False
    try:
        webpush(
            subscription_info={
                'endpoint': subscription.endpoint,
                'keys': {'p256dh': subscription.p256dh, 'auth': subscription.auth},
            },
            data=json.dumps(payload, ensure_ascii=False),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims=_vapid_claims(),
        )
        return True
    except WebPushException as exc:
        status = getattr(getattr(exc, 'response', None), 'status_code', None)
        if status in (404, 410):
            subscription.is_active = False
            subscription.save(update_fields=['is_active', 'updated_at'])
        logger.info('Web push failed for %s: %s', subscription.pk, exc)
        return False
    except Exception:
        logger.exception('Web push error for subscription %s', subscription.pk)
        return False


def subscriptions_for_order(order) -> Iterable[PushSubscription]:
    q = Q(is_active=True)
    email = (getattr(order, 'email', '') or '').strip().lower()
    parts = Q(pk__in=[])  # empty
    if order.user_id:
        parts |= Q(user_id=order.user_id)
    if email:
        parts |= Q(email__iexact=email)
    if order.user_id is None and not email:
        return PushSubscription.objects.none()
    return PushSubscription.objects.filter(q & parts).distinct()


def push_payload(*, title: str, body: str, url: str, tag: str) -> dict:
    return {
        'title': title,
        'body': body,
        'url': url,
        'tag': tag,
        'icon': '/static/img/pwa-192.png',
        'badge': '/static/img/pwa-192.png',
    }


def notify_order_push(order, *, kind: str) -> int:
    """kind: payment | status. Returns number of successful deliveries."""
    if not vapid_configured():
        return 0
    subs = list(subscriptions_for_order(order))
    if not subs:
        return 0

    status_labels = dict(order.STATUS_CHOICES)
    url = order.get_absolute_url()
    sent = 0
    prev = get_language()
    try:
        for sub in subs:
            lang = (sub.language or 'uk').strip() or 'uk'
            activate(lang)
            if kind == 'payment':
                title = _('Оплату підтверджено')
                body = _('Замовлення %(num)s оплачено.') % {'num': order.order_number}
                tag = f'order-pay-{order.order_number}'
            else:
                label = str(status_labels.get(order.status, order.status))
                title = _('Статус замовлення')
                body = _('Замовлення %(num)s: %(status)s') % {
                    'num': order.order_number,
                    'status': label,
                }
                tag = f'order-status-{order.order_number}-{order.status}'
            if send_web_push(sub, push_payload(title=title, body=body, url=url, tag=tag)):
                sent += 1
    finally:
        if prev:
            activate(prev)
    return sent
