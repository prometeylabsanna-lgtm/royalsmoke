from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_filters import RsBooleanDropdownFilter, dropdown_filter_options
from apps.core.admin_image_preview import ImagePreviewAdminMixin, image_thumb
from apps.core.admin_translation_forms import TranslationSyncModelForm
from apps.core.cms_i18n import lang_fields

from .models import (
    MobileBrand,
    MobileBrandFact,
    MobileBrandLine,
    MobileBrandPhoto,
    MobileHouseBlock,
    MobileLegalPage,
    MobileScreen,
    MobileSettings,
)


def _translated_bases(model) -> set[str]:
    from modeltranslation.translator import translator

    try:
        opts = translator.get_options_for_model(model)
    except Exception:
        return set()
    fields = getattr(opts, 'fields', None) or ()
    if isinstance(fields, dict):
        return set(fields)
    return set(fields)


def _is_hidden_widget(widget) -> bool:
    if getattr(widget, 'is_hidden', False) or isinstance(widget, forms.HiddenInput):
        return True
    inner = getattr(widget, 'widget', None)
    return isinstance(inner, forms.HiddenInput)


class _UkSharedFieldsMixin:
    """Неперекладні поля лишаються на вкладці UA: їх ховає той самий cms_lang_switch.js."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is None or getattr(db_field, 'language', None):
            return formfield
        if db_field.name in _translated_bases(db_field.model):
            return formfield
        if _is_hidden_widget(formfield.widget):
            return formfield
        formfield.widget.attrs['data-cms-lang'] = 'uk'
        return formfield


class _UkInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        field = form.fields.get('DELETE')
        if field is None or _is_hidden_widget(field.widget):
            return
        field.widget.attrs['data-cms-lang'] = 'uk'


class _MobileModelAdmin(_UkSharedFieldsMixin, ModelAdmin):
    change_form_template = 'admin/mobile/change_form.html'


class MobileSettingsAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileSettings
        fields = '__all__'


class MobileBrandAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileBrand
        fields = '__all__'


class MobileBrandFactAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileBrandFact
        fields = '__all__'


class MobileScreenAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileScreen
        fields = '__all__'


class MobileHouseBlockAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileHouseBlock
        fields = '__all__'


class MobileLegalPageAdminForm(TranslationSyncModelForm):
    class Meta:
        model = MobileLegalPage
        fields = '__all__'


class _MobileInline(_UkSharedFieldsMixin, TabularInline):
    formset = _UkInlineFormSet
    extra = 0


class MobileBrandFactInline(_MobileInline):
    model = MobileBrandFact
    form = MobileBrandFactAdminForm
    fields = (*lang_fields('label', 'value'), 'sort_order')


class MobileBrandLineInline(_MobileInline):
    model = MobileBrandLine
    fields = ('name', 'sort_order')
    classes = ('rs-cms-uk-only',)


class MobileBrandPhotoInline(ImagePreviewAdminMixin, _MobileInline):
    model = MobileBrandPhoto
    readonly_fields = ('image_preview',)
    fields = ('image_preview', 'image', 'sort_order', 'is_active')
    classes = ('rs-cms-uk-only',)

    def image_preview(self, obj):
        return image_thumb(getattr(obj, 'image', None), 'фото')
    image_preview.short_description = 'Превʼю'


class MobileHouseBlockInline(_MobileInline):
    model = MobileHouseBlock
    form = MobileHouseBlockAdminForm
    fields = ('index_label', *lang_fields('title', 'body'), 'sort_order')


@admin.register(MobileSettings)
class MobileSettingsAdmin(ImagePreviewAdminMixin, _MobileModelAdmin):
    form = MobileSettingsAdminForm
    list_display = ('__str__', 'contact_phone', 'app_version', 'seal_preview')
    fields = (
        'app_version',
        *lang_fields('app_blurb'),
        'app_seal',
        *lang_fields('contact_address'),
        'contact_phone',
        *lang_fields('contact_hours'),
        'contact_lat',
        'contact_lng',
    )

    def seal_preview(self, obj):
        return image_thumb(obj.app_seal, 'seal')
    seal_preview.short_description = 'Печатка'

    def has_add_permission(self, request):
        return not MobileSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MobileBrand)
class MobileBrandAdmin(ImagePreviewAdminMixin, _MobileModelAdmin):
    form = MobileBrandAdminForm
    list_display = ('cover_preview', 'name', 'country', 'panel', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    list_filter = (('is_active', RsBooleanDropdownFilter), 'panel')
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'is_active', 'panel',
        labels={'is_active': 'Активність', 'panel': 'Панель'},
    )
    search_fields = ('name', 'short_name', 'slug', 'country')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MobileBrandFactInline, MobileBrandLineInline, MobileBrandPhotoInline]
    fieldsets = (
        (None, {
            'fields': (
                'name', 'short_name', 'slug', 'mono',
                *lang_fields('country'),
                'panel', 'cover',
                *lang_fields('heritage'),
                'sort_order', 'is_active',
            ),
        }),
    )

    def cover_preview(self, obj):
        return image_thumb(obj.cover, obj.name)
    cover_preview.short_description = 'Обкладинка'


@admin.register(MobileScreen)
class MobileScreenAdmin(ImagePreviewAdminMixin, _MobileModelAdmin):
    form = MobileScreenAdminForm
    list_display = ('key', 'title', 'is_active', 'hero_preview', 'updated_at')
    list_filter = (('is_active', RsBooleanDropdownFilter),)
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options('is_active', labels={'is_active': 'Активність'})
    inlines = [MobileHouseBlockInline]
    fieldsets = (
        (None, {
            'fields': (
                'key', 'is_active',
                *lang_fields('kicker', 'title', 'subtitle', 'body', 'body_secondary'),
            ),
        }),
        ('Кнопки', {
            'fields': lang_fields('cta_primary', 'cta_secondary', 'confirm_label', 'legal_note'),
        }),
        ('Успіх (візит)', {
            'fields': lang_fields('success_title', 'success_body'),
            'classes': ('collapse',),
        }),
        ('Зображення', {
            'fields': ('hero_image',),
            'classes': ('rs-cms-uk-only',),
        }),
    )

    def hero_preview(self, obj):
        return image_thumb(obj.hero_image, obj.key)
    hero_preview.short_description = 'Фото'

    def get_inline_instances(self, request, obj=None):
        if obj is None or obj.key != MobileScreen.Key.HOUSE:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(MobileLegalPage)
class MobileLegalPageAdmin(_MobileModelAdmin):
    form = MobileLegalPageAdminForm
    list_display = ('title', 'slug', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = (('is_active', RsBooleanDropdownFilter),)
    list_filter_sheet = False
    search_fields = ('title', 'body')
    fields = (
        'slug',
        *lang_fields('title', 'body'),
        'is_active',
    )
