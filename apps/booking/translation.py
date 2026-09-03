from modeltranslation.translator import TranslationOptions, register

from .models import BookingService


@register(BookingService)
class BookingServiceTranslation(TranslationOptions):
    fields = ('title', 'description')
