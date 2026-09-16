from modeltranslation.translator import TranslationOptions, register

from .models import Product, ProductImage, ProductReview, ProductVariant
from .models_base import Brand, Category, ProductLine, Tag


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name', 'description', 'meta_title', 'meta_description')


@register(Brand)
class BrandTranslation(TranslationOptions):
    fields = ('name', 'short_description', 'description', 'country')


@register(ProductLine)
class ProductLineTranslation(TranslationOptions):
    fields = ('name', 'description')


@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = (
        'name', 'short_story', 'description', 'tasting_notes', 'recommendations',
        'wrapper', 'binder', 'filler', 'country', 'smoke_time',
        'meta_title', 'meta_description',
    )


@register(ProductVariant)
class ProductVariantTranslation(TranslationOptions):
    fields = ('name', 'shape')


@register(ProductImage)
class ProductImageTranslation(TranslationOptions):
    fields = ('alt_text',)


@register(ProductReview)
class ProductReviewTranslation(TranslationOptions):
    fields = ('text',)
