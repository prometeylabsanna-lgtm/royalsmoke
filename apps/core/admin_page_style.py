from __future__ import annotations

import re

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.core.admin_site_content_widgets import CmsAdminColorWidget
from apps.core.models import PageStyle
from apps.core.page_styles import ensure_page_styles, page_preview_url

_HEX_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')


def _clean_color(raw: str, *, default: str) -> str:
    value = (raw or '').strip()
    if not value:
        return ''
    if not _HEX_RE.match(value):
        raise forms.ValidationError('Очікується HEX, наприклад #100d0c')
    if len(value) == 4:
        value = f'#{value[1] * 2}{value[2] * 2}{value[3] * 2}'
    value = value.lower()
    if value == default.lower():
        return ''
    return value


class PageStyleAdminForm(forms.ModelForm):
    class Meta:
        model = PageStyle
        fields = ('background_color', 'text_color', 'accent_color')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        specs = (
            ('background_color', PageStyle.DEFAULT_BACKGROUND, 'Фон контенту'),
            ('text_color', PageStyle.DEFAULT_TEXT, 'Шрифт контенту'),
            ('accent_color', PageStyle.DEFAULT_ACCENT, 'Підсвітка контенту'),
        )
        for name, default, label in specs:
            field = self.fields[name]
            field.widget = CmsAdminColorWidget(default_color=default)
            field.label = label
            field.required = False
            current = (getattr(self.instance, name, '') or '').strip() or default
            field.initial = current
            field.help_text = (
                f'Тільки між шапкою і підвалом. Дефолт: {default}. '
                'Порожнє / дефолтний HEX = стиль сайту.'
            )

    def clean_background_color(self):
        return _clean_color(
            self.cleaned_data.get('background_color', ''),
            default=PageStyle.DEFAULT_BACKGROUND,
        )

    def clean_text_color(self):
        return _clean_color(
            self.cleaned_data.get('text_color', ''),
            default=PageStyle.DEFAULT_TEXT,
        )

    def clean_accent_color(self):
        return _clean_color(
            self.cleaned_data.get('accent_color', ''),
            default=PageStyle.DEFAULT_ACCENT,
        )


@admin.register(PageStyle)
class PageStyleAdmin(ModelAdmin):
    form = PageStyleAdminForm
    list_display = (
        'page',
        'swatch_bg',
        'swatch_text',
        'swatch_accent',
        'is_custom_display',
    )
    list_display_links = ('page',)
    readonly_fields = ('page',)
    fields = ('page', 'background_color', 'text_color', 'accent_color')
    ordering = ('page',)
    actions = ('reset_to_default_action',)
    change_form_template = 'admin/core/pagestyle/change_form.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ensure_page_styles()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST' and '_reset_default' in request.POST:
            obj = self.get_object(request, object_id)
            if obj is not None:
                obj.reset_to_default()
                self.message_user(
                    request, 'Скинуто до дефолтних кольорів сторінки', messages.SUCCESS,
                )
                return HttpResponseRedirect(
                    reverse('admin:core_pagestyle_change', args=[obj.pk]),
                )
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj is not None:
            extra_context['page_preview_base'] = page_preview_url(obj.page)
            extra_context['page_style_defaults'] = {
                'bg': PageStyle.DEFAULT_BACKGROUND,
                'text': PageStyle.DEFAULT_TEXT,
                'accent': PageStyle.DEFAULT_ACCENT,
            }
        return super().change_view(request, object_id, form_url, extra_context)

    def _swatch(self, color: str) -> str:
        return format_html(
            '<span class="rs-cms-colorpick__circle rs-cms-colorpick__circle--list" '
            'style="background:{};" title="{}"></span> <code>{}</code>',
            color, color, color,
        )

    @admin.display(description='Фон')
    def swatch_bg(self, obj: PageStyle):
        return self._swatch(obj.effective_background)

    @admin.display(description='Шрифт')
    def swatch_text(self, obj: PageStyle):
        return self._swatch(obj.effective_text)

    @admin.display(description='Підсвітка')
    def swatch_accent(self, obj: PageStyle):
        return self._swatch(obj.effective_accent)

    @admin.display(description='Кастомний', boolean=True)
    def is_custom_display(self, obj: PageStyle) -> bool:
        return obj.is_custom

    @admin.action(description='Скинути зміни до дефолту')
    def reset_to_default_action(self, request, queryset):
        for obj in queryset:
            obj.reset_to_default()
        self.message_user(request, 'Стилі скинуто до дефолту', messages.SUCCESS)
