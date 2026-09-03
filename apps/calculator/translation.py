from modeltranslation.translator import TranslationOptions, register

from .models import CalculatorOption, CalculatorQuestion


@register(CalculatorQuestion)
class CalculatorQuestionTranslation(TranslationOptions):
    fields = ('title', 'help_text')


@register(CalculatorOption)
class CalculatorOptionTranslation(TranslationOptions):
    fields = ('label', 'explanation')
