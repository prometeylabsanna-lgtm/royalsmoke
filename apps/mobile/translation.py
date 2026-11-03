from modeltranslation.translator import TranslationOptions, register

from .models import (
    MobileBrand,
    MobileBrandFact,
    MobileHouseBlock,
    MobileLegalPage,
    MobileScreen,
    MobileSettings,
)


@register(MobileSettings)
class MobileSettingsTranslation(TranslationOptions):
    fields = ('app_blurb', 'contact_address', 'contact_hours')


@register(MobileBrand)
class MobileBrandTranslation(TranslationOptions):
    fields = ('country', 'heritage')


@register(MobileBrandFact)
class MobileBrandFactTranslation(TranslationOptions):
    fields = ('label', 'value')


@register(MobileHouseBlock)
class MobileHouseBlockTranslation(TranslationOptions):
    fields = ('title', 'body')


@register(MobileScreen)
class MobileScreenTranslation(TranslationOptions):
    fields = (
        'kicker', 'title', 'subtitle', 'body', 'body_secondary',
        'cta_primary', 'cta_secondary', 'confirm_label', 'legal_note',
        'success_title', 'success_body',
    )


@register(MobileLegalPage)
class MobileLegalPageTranslation(TranslationOptions):
    fields = ('title', 'body')
