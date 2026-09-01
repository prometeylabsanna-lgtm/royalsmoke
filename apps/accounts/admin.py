from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from unfold.admin import ModelAdmin

from .models import DeliveryAddress, User, WishlistItem


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Профіль', {'fields': ('first_name', 'last_name', 'phone', 'preferred_language', 'market')}),
        ('Сповіщення', {'fields': ('notify_email', 'notify_telegram', 'telegram_chat_id')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Дати', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(ModelAdmin):
    list_display = ('user', 'label', 'city', 'is_default')


@admin.register(WishlistItem)
class WishlistItemAdmin(ModelAdmin):
    list_display = ('user', 'product', 'created_at')
