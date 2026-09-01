from modeltranslation.translator import TranslationOptions, register

from .models import Product, ProductReview
from .models_base import Brand, Category, ProductLine, Tag


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name', 'description', 'meta_title', 'meta_description')


@register(Brand)
class BrandTranslation(TranslationOptions):
    fields = ('name', 'short_description', 'description')


@register(ProductLine)
class ProductLineTranslation(TranslationOptions):
    fields = ('name', 'description')


@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = (
        'name', 'short_story', 'description', 'tasting_notes',
        'wrapper', 'binder', 'filler', 'country', 'smoke_time',
        'meta_title', 'meta_description',
    )


@register(ProductReview)
class ProductReviewTranslation(TranslationOptions):
    fields = ('text',)
