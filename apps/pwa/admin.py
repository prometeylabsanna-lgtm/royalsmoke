from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pwa.models import PushSubscription


@admin.register(PushSubscription)
class PushSubscriptionAdmin(ModelAdmin):
    list_display = (
        'id', 'email', 'user', 'language', 'is_active', 'updated_at',
    )
    list_filter = ('is_active', 'language')
    search_fields = ('email', 'endpoint', 'user__email')
    readonly_fields = ('endpoint', 'p256dh', 'auth', 'user_agent', 'created_at', 'updated_at')
