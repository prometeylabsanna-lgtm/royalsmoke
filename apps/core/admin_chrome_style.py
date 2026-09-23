from __future__ import annotations

import re

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.core.admin_site_content_widgets import CmsAdminColorWidget
from apps.core.models import ChromeStyle

_HEX_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

_FIELD_DEFAULTS = (
    ('header_bg', ChromeStyle.DEFAULT_HEADER_BG, 'Шапка — фон'),
    ('header_text', ChromeStyle.DEFAULT_HEADER_TEXT, 'Шапка — шрифт'),
    ('footer_top_bg', ChromeStyle.DEFAULT_FOOTER_TOP_BG, 'Підвал (верх) — фон'),
    ('footer_top_text', ChromeStyle.DEFAULT_FOOTER_TOP_TEXT, 'Підвал (верх) — шрифт'),
    ('footer_bottom_bg', ChromeStyle.DEFAULT_FOOTER_BOTTOM_BG, 'Підвал (низ) — фон'),
    ('footer_bottom_text', ChromeStyle.DEFAULT_FOOTER_BOTTOM_TEXT, 'Підвал (низ) — шрифт'),
)


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


class ChromeStyleAdminForm(forms.ModelForm):
    class Meta:
        model = ChromeStyle
        fields = [name for name, _default, _label in _FIELD_DEFAULTS]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, default, label in _FIELD_DEFAULTS:
            field = self.fields[name]
            field.widget = CmsAdminColorWidget(default_color=default)
            field.label = label
            field.required = False
            current = (getattr(self.instance, name, '') or '').strip() or default
            field.initial = current
            field.help_text = f'Дефолт: {default}. Порожнє / дефолтний HEX = стиль сайту.'

    def clean_header_bg(self):
        return _clean_color(self.cleaned_data.get('header_bg', ''), default=ChromeStyle.DEFAULT_HEADER_BG)

    def clean_header_text(self):
        return _clean_color(self.cleaned_data.get('header_text', ''), default=ChromeStyle.DEFAULT_HEADER_TEXT)

    def clean_footer_top_bg(self):
        return _clean_color(
            self.cleaned_data.get('footer_top_bg', ''),
            default=ChromeStyle.DEFAULT_FOOTER_TOP_BG,
        )

    def clean_footer_top_text(self):
        return _clean_color(
            self.cleaned_data.get('footer_top_text', ''),
            default=ChromeStyle.DEFAULT_FOOTER_TOP_TEXT,
        )

    def clean_footer_bottom_bg(self):
        return _clean_color(
            self.cleaned_data.get('footer_bottom_bg', ''),
            default=ChromeStyle.DEFAULT_FOOTER_BOTTOM_BG,
        )

    def clean_footer_bottom_text(self):
        return _clean_color(
            self.cleaned_data.get('footer_bottom_text', ''),
            default=ChromeStyle.DEFAULT_FOOTER_BOTTOM_TEXT,
        )


@admin.register(ChromeStyle)
class ChromeStyleAdmin(ModelAdmin):
    form = ChromeStyleAdminForm
    list_display = ('__str__', 'swatch_header', 'swatch_footer')
    fields = [name for name, _d, _l in _FIELD_DEFAULTS]
    actions = ('reset_to_default_action',)

    def has_add_permission(self, request):
        return not ChromeStyle.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = ChromeStyle.objects.get_or_create(pk=1)
        return HttpResponseRedirect(reverse('admin:core_chromestyle_change', args=[obj.pk]))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST' and '_reset_default' in request.POST:
            obj = self.get_object(request, object_id)
            if obj is not None:
                obj.reset_to_default()
                self.message_user(request, 'Шапка і підвал скинуто до дефолту', messages.SUCCESS)
                return HttpResponseRedirect(
                    reverse('admin:core_chromestyle_change', args=[obj.pk]),
                )
        return super().change_view(request, object_id, form_url, extra_context)

    def _swatch(self, color: str) -> str:
        return format_html(
            '<span class="rs-cms-colorpick__circle rs-cms-colorpick__circle--list" '
            'style="background:{};" title="{}"></span> <code>{}</code>',
            color, color, color,
        )

    @admin.display(description='Шапка')
    def swatch_header(self, obj: ChromeStyle):
        eff = obj.effective()
        return self._swatch(eff['header_bg'])

    @admin.display(description='Підвал')
    def swatch_footer(self, obj: ChromeStyle):
        eff = obj.effective()
        return self._swatch(eff['footer_bottom_bg'])

    @admin.action(description='Скинути до дефолту')
    def reset_to_default_action(self, request, queryset):
        for obj in queryset:
            obj.reset_to_default()
        self.message_user(request, 'Скинуто до дефолту', messages.SUCCESS)
