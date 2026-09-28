from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_filters import RsBooleanDropdownFilter, dropdown_filter_options
from apps.core.admin_image_preview import ImagePreviewAdminMixin, image_thumb

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


class MobileBrandFactInline(TabularInline):
    model = MobileBrandFact
    extra = 0


class MobileBrandLineInline(TabularInline):
    model = MobileBrandLine
    extra = 0


class MobileBrandPhotoInline(TabularInline):
    model = MobileBrandPhoto
    extra = 0
    readonly_fields = ('image_preview',)
    fields = ('image_preview', 'image', 'sort_order', 'is_active')

    def image_preview(self, obj):
        return image_thumb(getattr(obj, 'image', None), 'фото')
    image_preview.short_description = 'Превʼю'


class MobileHouseBlockInline(TabularInline):
    model = MobileHouseBlock
    extra = 0


@admin.register(MobileSettings)
class MobileSettingsAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = ('__str__', 'contact_phone', 'app_version', 'seal_preview')
    fields = (
        'app_version',
        'app_blurb',
        'app_seal',
        'contact_address',
        'contact_phone',
        'contact_hours',
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
class MobileBrandAdmin(ImagePreviewAdminMixin, ModelAdmin):
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
                'name', 'short_name', 'slug', 'mono', 'country', 'panel',
                'cover', 'heritage', 'sort_order', 'is_active',
            ),
        }),
    )

    def cover_preview(self, obj):
        return image_thumb(obj.cover, obj.name)
    cover_preview.short_description = 'Обкладинка'


@admin.register(MobileScreen)
class MobileScreenAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = ('key', 'title', 'is_active', 'hero_preview', 'updated_at')
    list_filter = (('is_active', RsBooleanDropdownFilter),)
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options('is_active', labels={'is_active': 'Активність'})
    inlines = [MobileHouseBlockInline]
    fieldsets = (
        (None, {
            'fields': ('key', 'is_active', 'kicker', 'title', 'subtitle', 'body', 'body_secondary'),
        }),
        ('Кнопки', {
            'fields': ('cta_primary', 'cta_secondary', 'confirm_label', 'legal_note'),
        }),
        ('Успіх (візит)', {
            'fields': ('success_title', 'success_body'),
            'classes': ('collapse',),
        }),
        ('Зображення', {
            'fields': ('hero_image',),
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
class MobileLegalPageAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = (('is_active', RsBooleanDropdownFilter),)
    list_filter_sheet = False
    search_fields = ('title', 'body')
