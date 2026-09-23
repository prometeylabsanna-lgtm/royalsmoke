from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.cart.models import Cart, CartItem, CartReservation


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'updated_at', 'created_at')
    search_fields = ('user__email',)
    inlines = [CartItemInline]


@admin.register(CartReservation)
class CartReservationAdmin(ModelAdmin):
    list_display = ('product', 'quantity', 'user', 'session_key', 'expires_at', 'updated_at')
    list_filter = ('expires_at',)
    search_fields = ('session_key', 'user__email', 'product__name')
    raw_id_fields = ('product', 'user')
