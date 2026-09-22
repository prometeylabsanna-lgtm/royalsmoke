from modeltranslation.translator import TranslationOptions, register

from .models import BlogFAQItem, BlogPost, FAQItem, LegalDocument


@register(FAQItem)
class FAQItemTranslation(TranslationOptions):
    fields = ('question', 'answer')


@register(LegalDocument)
class LegalDocumentTranslation(TranslationOptions):
    fields = ('title', 'body')


@register(BlogPost)
class BlogPostTranslation(TranslationOptions):
    fields = (
        'title', 'excerpt', 'body', 'cover_alt',
        'meta_title', 'meta_description',
    )


@register(BlogFAQItem)
class BlogFAQItemTranslation(TranslationOptions):
    fields = ('question', 'answer')
