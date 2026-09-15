from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from apps.orders.services import nova_poshta as np_svc

from .models import Order, OrderItem, Payment


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product', 'variant', 'product_name', 'variant_name',
        'product_sku', 'price', 'quantity', 'line_total',
    )


class PaymentInline(TabularInline):
    model = Payment
    extra = 0
    readonly_fields = (
        'provider', 'status', 'amount', 'currency',
        'liqpay_order_id', 'transaction_id', 'created_at', 'updated_at',
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'order_number', 'status', 'first_name', 'last_name',
        'phone', 'total', 'np_ttn', 'created_at',
    )
    list_filter = ('status', 'payment_method', 'delivery_service')
    search_fields = ('order_number', 'phone', 'email', 'first_name', 'last_name', 'np_ttn')
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ('order_number', 'idempotency_key', 'created_at', 'updated_at', 'np_ttn', 'np_ttn_ref')
    actions = ('create_ttn_action', 'refresh_ttn_status')

    @admin.action(description=_('Створити ТТН Нової Пошти'))
    def create_ttn_action(self, request, queryset):
        ok = 0
        for order in queryset:
            if order.np_ttn:
                continue
            if order.delivery_service != Order.DELIVERY_NP:
                continue
            if not order.np_city_ref or not order.np_warehouse_ref:
                continue
            try:
                result = np_svc.create_ttn(order)
                order.np_ttn = result['ttn']
                order.np_ttn_ref = result['ref']
                if order.status in (Order.STATUS_PAID, Order.STATUS_PENDING, Order.STATUS_PROCESSING):
                    order.status = Order.STATUS_PROCESSING
                order.save(update_fields=['np_ttn', 'np_ttn_ref', 'status', 'updated_at'])
                ok += 1
            except np_svc.NovaPoshtaError as exc:
                self.message_user(request, f'{order.order_number}: {exc}', level=messages.ERROR)
        self.message_user(request, _('Створено ТТН: %(n)s') % {'n': ok})

    @admin.action(description=_('Оновити статус ТТН'))
    def refresh_ttn_status(self, request, queryset):
        # NP status codes: 9/10/11 delivered-ish; 7/8 arriving; etc.
        delivered_codes = {'9', '10', '11'}
        shipped_codes = {'4', '5', '6', '7', '8', '101'}
        updated = 0
        for order in queryset.filter(np_ttn__gt=''):
            try:
                info = np_svc.track_ttn(order.np_ttn)
            except np_svc.NovaPoshtaError as exc:
                self.message_user(request, f'{order.order_number}: {exc}', level=messages.ERROR)
                continue
            code = info.get('status_code') or ''
            if code in delivered_codes and order.status != Order.STATUS_DONE:
                order.status = Order.STATUS_DONE
                order.save(update_fields=['status', 'updated_at'])
                updated += 1
            elif code in shipped_codes and order.status not in (Order.STATUS_SHIPPED, Order.STATUS_DONE):
                order.status = Order.STATUS_SHIPPED
                order.save(update_fields=['status', 'updated_at'])
                updated += 1
        self.message_user(request, _('Оновлено статусів: %(n)s') % {'n': updated})


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('liqpay_order_id', 'order', 'status', 'amount', 'currency', 'created_at')
    list_filter = ('status', 'provider')
    search_fields = ('liqpay_order_id', 'transaction_id', 'order__order_number')
    readonly_fields = ('raw_callback', 'created_at', 'updated_at')
