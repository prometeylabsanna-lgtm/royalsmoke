from modeltranslation.translator import TranslationOptions, register

from .models import FAQItem, LegalDocument


@register(FAQItem)
class FAQItemTranslation(TranslationOptions):
    fields = ('question', 'answer')


@register(LegalDocument)
class LegalDocumentTranslation(TranslationOptions):
    fields = ('title', 'body')
