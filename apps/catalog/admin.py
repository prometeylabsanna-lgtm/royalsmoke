from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Product, ProductImage, ProductReview, ProductVariant
from .models_base import Brand, Category, ProductLine, Tag


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'kind', 'parent', 'is_active', 'is_featured', 'sort_order')
    list_filter = ('kind', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'country', 'is_active', 'is_featured', 'sort_order')
    list_filter = ('is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(ProductLine)
class ProductLineAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'is_active', 'sort_order')
    list_filter = ('brand', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        'name', 'brand', 'category', 'strength', 'country',
        'base_price', 'is_active', 'is_featured',
    )
    list_filter = ('is_active', 'strength', 'country', 'brand', 'category', 'tags')
    search_fields = ('name', 'sku', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ('product', 'author_name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
