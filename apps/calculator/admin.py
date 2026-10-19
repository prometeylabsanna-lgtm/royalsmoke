from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.cms_i18n import lang_fields

from .models import CalculatorOption, CalculatorQuestion


class CalculatorOptionInline(TabularInline):
    model = CalculatorOption
    extra = 1
    show_title = False
    fields = (
        *lang_fields('label'),
        'value', 'filter_field', 'filter_value',
        *lang_fields('explanation'),
        'sort_order', 'is_active',
    )


@admin.register(CalculatorQuestion)
class CalculatorQuestionAdmin(ModelAdmin):
    list_display = ('title', 'step_key', 'sort_order', 'is_active')
    inlines = [CalculatorOptionInline]
