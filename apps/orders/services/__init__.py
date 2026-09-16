from __future__ import annotations

from django.utils.translation import gettext as _

from apps.core.services.notifications import notify_admins, notify_user, render_email


def notify_order_created(order) -> None:
    ctx = {'order': order}
    text, html = render_email('order_created', ctx)
    notify_admins(
        f'Нове замовлення {order.order_number}',
        text,
        html=html,
        telegram_text=(
            f'🛒 Замовлення {order.order_number}\n'
            f'{order.total} {order.currency}\n'
            f'{order.first_name} {order.last_name}\n'
            f'{order.phone}'
        ),
    )
    cust_text, cust_html = render_email('order_created_customer', ctx)
    notify_user(
        order.email,
        _('Замовлення %(num)s прийнято') % {'num': order.order_number},
        cust_text,
        html=cust_html,
        user=order.user,
    )


def notify_order_paid(order) -> None:
    ctx = {'order': order}
    text, html = render_email('order_paid', ctx)
    notify_admins(
        f'Оплачено {order.order_number}',
        text,
        html=html,
        telegram_text=f'💳 Оплачено {order.order_number} — {order.total} {order.currency}',
    )
    notify_user(
        order.email,
        _('Оплату замовлення %(num)s підтверджено') % {'num': order.order_number},
        text,
        html=html,
        user=order.user,
    )
