from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_filters import (
    RsAllValuesDropdownFilter,
    RsBooleanDropdownFilter,
    RsChoicesDropdownFilter,
    RsRelatedDropdownFilter,
    dropdown_filter_options,
)
from apps.core.admin_image_preview import ImagePreviewAdminMixin, image_thumb

from .models import Product, ProductImage, ProductReview, ProductVariant
from .models_base import Brand, Category, ProductLine, Tag


class ProductImageInline(ImagePreviewAdminMixin, TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'sort_order', 'is_primary')


class ProductVariantInline(ImagePreviewAdminMixin, TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = ('image_preview', 'name', 'kind', 'parent', 'is_active', 'is_featured', 'sort_order')
    list_filter = (
        ('kind', RsChoicesDropdownFilter),
        ('is_active', RsBooleanDropdownFilter),
        ('is_featured', RsBooleanDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'kind', 'is_active', 'is_featured',
        labels={'is_active': 'Активність', 'is_featured': 'Рекомендовані'},
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def image_preview(self, obj):
        return image_thumb(obj.image, obj.name)
    image_preview.short_description = 'Фото'


@admin.register(Brand)
class BrandAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = ('logo_preview', 'name', 'country', 'is_active', 'is_featured', 'sort_order')
    list_filter = (
        ('is_active', RsBooleanDropdownFilter),
        ('is_featured', RsBooleanDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'is_active', 'is_featured',
        labels={'is_active': 'Активність', 'is_featured': 'Рекомендовані'},
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def logo_preview(self, obj):
        return image_thumb(obj.logo, obj.name)
    logo_preview.short_description = 'Лого'


@admin.register(ProductLine)
class ProductLineAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = ('image_preview', 'name', 'brand', 'is_active', 'sort_order')
    list_filter = (
        ('brand', RsRelatedDropdownFilter),
        ('is_active', RsBooleanDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'brand', 'is_active',
        labels={'is_active': 'Активність'},
    )
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        return image_thumb(obj.image, obj.name)
    image_preview.short_description = 'Фото'


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ImagePreviewAdminMixin, ModelAdmin):
    list_display = (
        'image_preview', 'name', 'brand', 'category', 'strength', 'country',
        'base_price', 'is_active', 'is_featured',
    )
    list_filter = (
        ('is_active', RsBooleanDropdownFilter),
        ('strength', RsChoicesDropdownFilter),
        ('country', RsAllValuesDropdownFilter),
        ('brand', RsRelatedDropdownFilter),
        ('category', RsRelatedDropdownFilter),
        ('tags', RsRelatedDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'is_active', 'strength', 'country', 'brand', 'category', 'tags',
        labels={
            'is_active': 'Активність',
            'strength': 'Міцність',
            'country': 'Країна виробника',
        },
    )
    search_fields = ('name', 'sku', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)
    inlines = [ProductVariantInline, ProductImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images')

    def image_preview(self, obj):
        img = next((item for item in obj.images.all() if item.is_primary), None)
        if img is None:
            img = next(iter(obj.images.all()), None)
        if img is None:
            return '—'
        return image_thumb(img.image, obj.name)
    image_preview.short_description = 'Фото'


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ('product', 'author_name', 'rating', 'is_published', 'created_at')
    list_filter = (
        ('is_published', RsBooleanDropdownFilter),
        ('rating', RsAllValuesDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'is_published', 'rating',
        labels={'is_published': 'Опубліковано'},
    )
