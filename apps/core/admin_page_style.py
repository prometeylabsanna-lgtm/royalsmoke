from __future__ import annotations

import re

from django import forms
from django.contrib import admin, messages
from django.db.models import Case, IntegerField, When
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.core.admin_site_content_widgets import CmsAdminColorWidget
from apps.core.models import ChromeStyle, PageStyle, SiteBlock
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


def _bind_color_field(field, *, default: str, label: str, current: str, help_extra: str = '') -> None:
    field.widget = CmsAdminColorWidget(default_color=default)
    field.label = label
    field.required = False
    field.initial = (current or '').strip() or default
    field.help_text = (
        f'{help_extra}Дефолт: {default}. Порожнє / дефолтний HEX = стиль сайту.'
    ).strip()


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
            _bind_color_field(
                self.fields[name],
                default=default,
                label=label,
                current=getattr(self.instance, name, '') or '',
                help_extra='Тільки між шапкою і підвалом. ',
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


class HeaderStyleAdminForm(forms.ModelForm):
    """Редагує ChromeStyle.header_* через рядок PageStyle «Шапка сайту»."""

    class Meta:
        model = PageStyle
        fields = ('background_color', 'text_color')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome = ChromeStyle.load()
        _bind_color_field(
            self.fields['background_color'],
            default=ChromeStyle.DEFAULT_HEADER_BG,
            label='Шапка — фон',
            current=chrome.header_bg,
        )
        _bind_color_field(
            self.fields['text_color'],
            default=ChromeStyle.DEFAULT_HEADER_TEXT,
            label='Шапка — шрифт',
            current=chrome.header_text,
        )

    def clean_background_color(self):
        return _clean_color(
            self.cleaned_data.get('background_color', ''),
            default=ChromeStyle.DEFAULT_HEADER_BG,
        )

    def clean_text_color(self):
        return _clean_color(
            self.cleaned_data.get('text_color', ''),
            default=ChromeStyle.DEFAULT_HEADER_TEXT,
        )

    def save(self, commit=True):
        chrome = ChromeStyle.load()
        chrome.header_bg = self.cleaned_data.get('background_color', '')
        chrome.header_text = self.cleaned_data.get('text_color', '')
        chrome.save()
        obj = super().save(commit=False)
        obj.background_color = chrome.header_bg
        obj.text_color = chrome.header_text
        obj.accent_color = ''
        if commit:
            obj.save()
        return obj


class FooterStyleAdminForm(forms.ModelForm):
    """Редагує ChromeStyle.footer_* через рядок PageStyle «Підвал»."""

    footer_top_bg = forms.CharField(required=False)
    footer_top_text = forms.CharField(required=False)
    footer_bottom_bg = forms.CharField(required=False)
    footer_bottom_text = forms.CharField(required=False)

    class Meta:
        model = PageStyle
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome = ChromeStyle.load()
        specs = (
            ('footer_top_bg', ChromeStyle.DEFAULT_FOOTER_TOP_BG, 'Підвал (верх) — фон', chrome.footer_top_bg),
            ('footer_top_text', ChromeStyle.DEFAULT_FOOTER_TOP_TEXT, 'Підвал (верх) — шрифт', chrome.footer_top_text),
            ('footer_bottom_bg', ChromeStyle.DEFAULT_FOOTER_BOTTOM_BG, 'Підвал (низ) — фон', chrome.footer_bottom_bg),
            ('footer_bottom_text', ChromeStyle.DEFAULT_FOOTER_BOTTOM_TEXT, 'Підвал (низ) — шрифт', chrome.footer_bottom_text),
        )
        for name, default, label, current in specs:
            _bind_color_field(self.fields[name], default=default, label=label, current=current)

    def clean_footer_top_bg(self):
        return _clean_color(self.cleaned_data.get('footer_top_bg', ''), default=ChromeStyle.DEFAULT_FOOTER_TOP_BG)

    def clean_footer_top_text(self):
        return _clean_color(self.cleaned_data.get('footer_top_text', ''), default=ChromeStyle.DEFAULT_FOOTER_TOP_TEXT)

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

    def save(self, commit=True):
        chrome = ChromeStyle.load()
        chrome.footer_top_bg = self.cleaned_data.get('footer_top_bg', '')
        chrome.footer_top_text = self.cleaned_data.get('footer_top_text', '')
        chrome.footer_bottom_bg = self.cleaned_data.get('footer_bottom_bg', '')
        chrome.footer_bottom_text = self.cleaned_data.get('footer_bottom_text', '')
        chrome.save()
        obj = super().save(commit=False)
        obj.background_color = chrome.footer_bottom_bg
        obj.text_color = chrome.footer_bottom_text
        obj.accent_color = chrome.footer_top_bg
        if commit:
            obj.save()
        return obj


@admin.register(PageStyle)
class PageStyleAdmin(ModelAdmin):
    list_display = (
        'page',
        'swatch_bg',
        'swatch_text',
        'swatch_accent',
        'is_custom_display',
    )
    list_display_links = ('page',)
    readonly_fields = ('page',)
    actions = ('reset_to_default_action',)
    change_form_template = 'admin/core/pagestyle/change_form.html'

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is not None:
            if obj.page == SiteBlock.Page.HEADER:
                return HeaderStyleAdminForm
            if obj.page == SiteBlock.Page.FOOTER:
                return FooterStyleAdminForm
        return PageStyleAdminForm

    def get_fields(self, request, obj=None):
        if obj is not None and obj.page == SiteBlock.Page.HEADER:
            return ('page', 'background_color', 'text_color')
        if obj is not None and obj.page == SiteBlock.Page.FOOTER:
            return ('page', 'footer_top_bg', 'footer_top_text', 'footer_bottom_bg', 'footer_bottom_text')
        return ('page', 'background_color', 'text_color', 'accent_color')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _chrome_order=Case(
                When(page=SiteBlock.Page.HEADER, then=0),
                When(page=SiteBlock.Page.FOOTER, then=1),
                default=2,
                output_field=IntegerField(),
            ),
        ).order_by('_chrome_order', 'page')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ensure_page_styles()
        ChromeStyle.load()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if request.method == 'POST' and '_reset_default' in request.POST and obj is not None:
            self._reset_obj(obj)
            self.message_user(request, 'Скинуто до дефолтних кольорів', messages.SUCCESS)
            return HttpResponseRedirect(
                reverse('admin:core_pagestyle_change', args=[obj.pk]),
            )
        extra_context = extra_context or {}
        if obj is not None:
            extra_context['page_preview_base'] = page_preview_url(obj.page)
            if obj.page == SiteBlock.Page.HEADER:
                extra_context['page_style_defaults'] = {
                    'bg': ChromeStyle.DEFAULT_HEADER_BG,
                    'text': ChromeStyle.DEFAULT_HEADER_TEXT,
                    'accent': PageStyle.DEFAULT_ACCENT,
                }
                extra_context['hide_page_style_preview'] = True
            elif obj.page == SiteBlock.Page.FOOTER:
                extra_context['page_style_defaults'] = {
                    'bg': ChromeStyle.DEFAULT_FOOTER_BOTTOM_BG,
                    'text': ChromeStyle.DEFAULT_FOOTER_BOTTOM_TEXT,
                    'accent': ChromeStyle.DEFAULT_FOOTER_TOP_BG,
                }
                extra_context['hide_page_style_preview'] = True
            else:
                extra_context['page_style_defaults'] = {
                    'bg': PageStyle.DEFAULT_BACKGROUND,
                    'text': PageStyle.DEFAULT_TEXT,
                    'accent': PageStyle.DEFAULT_ACCENT,
                }
        return super().change_view(request, object_id, form_url, extra_context)

    def _reset_obj(self, obj: PageStyle) -> None:
        chrome = ChromeStyle.load()
        if obj.page == SiteBlock.Page.HEADER:
            chrome.header_bg = ''
            chrome.header_text = ''
            chrome.save(update_fields=['header_bg', 'header_text'])
            obj.background_color = ''
            obj.text_color = ''
            obj.accent_color = ''
            obj.save(update_fields=['background_color', 'text_color', 'accent_color'])
            return
        if obj.page == SiteBlock.Page.FOOTER:
            chrome.footer_top_bg = ''
            chrome.footer_top_text = ''
            chrome.footer_bottom_bg = ''
            chrome.footer_bottom_text = ''
            chrome.save(update_fields=[
                'footer_top_bg', 'footer_top_text',
                'footer_bottom_bg', 'footer_bottom_text',
            ])
            obj.background_color = ''
            obj.text_color = ''
            obj.accent_color = ''
            obj.save(update_fields=['background_color', 'text_color', 'accent_color'])
            return
        obj.reset_to_default()

    def _chrome_eff(self) -> dict[str, str]:
        return ChromeStyle.load().effective()

    def _swatch(self, color: str) -> str:
        return format_html(
            '<span class="rs-cms-colorpick__circle rs-cms-colorpick__circle--list" '
            'style="background:{};" title="{}"></span> <code>{}</code>',
            color, color, color,
        )

    @admin.display(description='Фон')
    def swatch_bg(self, obj: PageStyle):
        if obj.page == SiteBlock.Page.HEADER:
            return self._swatch(self._chrome_eff()['header_bg'])
        if obj.page == SiteBlock.Page.FOOTER:
            return self._swatch(self._chrome_eff()['footer_bottom_bg'])
        return self._swatch(obj.effective_background)

    @admin.display(description='Шрифт')
    def swatch_text(self, obj: PageStyle):
        if obj.page == SiteBlock.Page.HEADER:
            return self._swatch(self._chrome_eff()['header_text'])
        if obj.page == SiteBlock.Page.FOOTER:
            return self._swatch(self._chrome_eff()['footer_bottom_text'])
        return self._swatch(obj.effective_text)

    @admin.display(description='Підсвітка')
    def swatch_accent(self, obj: PageStyle):
        if obj.page == SiteBlock.Page.HEADER:
            return format_html('<span class="text-font-subtle">—</span>')
        if obj.page == SiteBlock.Page.FOOTER:
            return self._swatch(self._chrome_eff()['footer_top_bg'])
        return self._swatch(obj.effective_accent)

    @admin.display(description='Кастомний', boolean=True)
    def is_custom_display(self, obj: PageStyle) -> bool:
        if obj.page == SiteBlock.Page.HEADER:
            chrome = ChromeStyle.load()
            return bool((chrome.header_bg or '').strip() or (chrome.header_text or '').strip())
        if obj.page == SiteBlock.Page.FOOTER:
            chrome = ChromeStyle.load()
            return bool(
                (chrome.footer_top_bg or '').strip()
                or (chrome.footer_top_text or '').strip()
                or (chrome.footer_bottom_bg or '').strip()
                or (chrome.footer_bottom_text or '').strip()
            )
        return obj.is_custom

    @admin.action(description='Скинути зміни до дефолту')
    def reset_to_default_action(self, request, queryset):
        for obj in queryset:
            self._reset_obj(obj)
        self.message_user(request, 'Стилі скинуто до дефолту', messages.SUCCESS)
