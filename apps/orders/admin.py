from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product', 'variant', 'product_name', 'variant_name',
        'product_sku', 'price', 'quantity', 'line_total',
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'order_number', 'status', 'first_name', 'last_name',
        'phone', 'total', 'created_at',
    )
    list_filter = ('status', 'payment_method', 'delivery_service')
    search_fields = ('order_number', 'phone', 'email', 'first_name', 'last_name')
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'idempotency_key', 'created_at', 'updated_at')
