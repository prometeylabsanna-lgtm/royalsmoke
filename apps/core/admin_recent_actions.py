from __future__ import annotations

from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

# Підписи в меню / заголовку сторінки
LogEntry._meta.verbose_name = 'Недавня дія'
LogEntry._meta.verbose_name_plural = 'Недавні дії'


@admin.register(LogEntry)
class RecentActionsAdmin(ModelAdmin):
    """Окрема сторінка «Недавні дії» в сайдбарі."""

    list_display = (
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_label',
    )
    list_display_links = ('action_time',)
    list_filter = ('action_flag', 'content_type')
    search_fields = ('object_repr', 'change_message', 'user__email', 'user__username')
    date_hierarchy = 'action_time'
    ordering = ('-action_time',)
    list_per_page = 50
    readonly_fields = (
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message',
    )
    fields = readonly_fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_staff

    @admin.display(description='Обʼєкт')
    def object_link(self, obj: LogEntry):
        text = obj.object_repr or '—'
        if obj.action_flag == DELETION or not obj.content_type_id or not obj.object_id:
            return text
        try:
            url = reverse(
                f'admin:{obj.content_type.app_label}_{obj.content_type.model}_change',
                args=[obj.object_id],
            )
        except NoReverseMatch:
            return text
        return format_html('<a href="{}">{}</a>', url, text)

    @admin.display(description='Дія')
    def action_label(self, obj: LogEntry) -> str:
        return {
            ADDITION: 'Додано',
            CHANGE: 'Змінено',
            DELETION: 'Видалено',
        }.get(obj.action_flag, str(obj.get_action_flag_display()))
