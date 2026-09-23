from __future__ import annotations

import re

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from apps.core.admin_site_content_widgets import CmsAdminColorWidget
from apps.core.models import PageStyle
from apps.core.page_styles import ensure_page_styles

_HEX_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')


class PageStyleAdminForm(forms.ModelForm):
    class Meta:
        model = PageStyle
        fields = ('background_color',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = (self.instance.background_color or '').strip() or PageStyle.DEFAULT_BACKGROUND
        self.fields['background_color'].widget = CmsAdminColorWidget()
        self.fields['background_color'].initial = color
        self.fields['background_color'].required = False
        self.fields['background_color'].help_text = (
            f'Дефолт сайту: {PageStyle.DEFAULT_BACKGROUND}. '
            'Кнопка «Скинути до дефолту» очищає кастомний колір.'
        )

    def clean_background_color(self):
        raw = (self.cleaned_data.get('background_color') or '').strip()
        if not raw:
            return ''
        if not _HEX_RE.match(raw):
            raise forms.ValidationError('Очікується HEX, наприклад #100d0c')
        if raw.lower() == PageStyle.DEFAULT_BACKGROUND.lower():
            return ''
        return raw.lower()


@admin.register(PageStyle)
class PageStyleAdmin(ModelAdmin):
    form = PageStyleAdminForm
    list_display = ('page', 'background_color_display', 'is_custom_display')
    list_display_links = ('page',)
    readonly_fields = ('page',)
    fields = ('page', 'background_color')
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
                    request, 'Скинуто до дефолтного кольору фону', messages.SUCCESS,
                )
                return HttpResponseRedirect(
                    reverse('admin:core_pagestyle_change', args=[obj.pk]),
                )
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description='Колір')
    def background_color_display(self, obj: PageStyle) -> str:
        return obj.effective_color

    @admin.display(description='Кастомний', boolean=True)
    def is_custom_display(self, obj: PageStyle) -> bool:
        return obj.is_custom

    @admin.action(description='Скинути зміни до дефолту')
    def reset_to_default_action(self, request, queryset):
        for obj in queryset:
            obj.reset_to_default()
        self.message_user(request, 'Стилі скинуто до дефолту', messages.SUCCESS)
