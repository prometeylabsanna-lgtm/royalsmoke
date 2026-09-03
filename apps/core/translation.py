from modeltranslation.translator import TranslationOptions, register

from .models import HeroSlide, HistorySlide, SiteBlock, SiteSettings


@register(SiteSettings)
class SiteSettingsTranslation(TranslationOptions):
    fields = ('site_name', 'address', 'work_hours', 'meta_description')


@register(SiteBlock)
class SiteBlockTranslation(TranslationOptions):
    fields = ('text_html',)


@register(HeroSlide)
class HeroSlideTranslation(TranslationOptions):
    fields = (
        'title', 'subtitle',
        'cta_primary_label', 'cta_secondary_label',
    )


@register(HistorySlide)
class HistorySlideTranslation(TranslationOptions):
    fields = ('year_label', 'title', 'text', 'cta_label')
