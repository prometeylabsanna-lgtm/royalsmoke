from __future__ import annotations

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.orders.models import Order


@receiver(pre_save, sender=Order)
def _order_status_remember(sender, instance: Order, **kwargs):
    if not instance.pk:
        instance._pwa_prev_status = None
        return
    instance._pwa_prev_status = (
        Order.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    )


@receiver(post_save, sender=Order)
def _order_status_push(sender, instance: Order, created: bool, **kwargs):
    if created:
        return
    prev = getattr(instance, '_pwa_prev_status', None)
    if prev is None or prev == instance.status:
        return
    # Payment confirmation is sent from settle_payment path (kind=payment).
    if instance.status == Order.STATUS_PAID:
        return
    order_pk = instance.pk

    def _send():
        from apps.pwa.services.push import notify_order_push

        notify_order_push(Order.objects.get(pk=order_pk), kind='status')

    transaction.on_commit(_send)
