from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import CalculatorOption, CalculatorQuestion


class CalculatorOptionInline(TabularInline):
    model = CalculatorOption
    extra = 1
    show_title = False
    fields = (
        'label_uk', 'label_en', 'label_zh_hans',
        'value', 'filter_field', 'filter_value',
        'explanation_uk', 'explanation_en', 'explanation_zh_hans',
        'sort_order', 'is_active',
    )


@admin.register(CalculatorQuestion)
class CalculatorQuestionAdmin(ModelAdmin):
    list_display = ('title', 'step_key', 'sort_order', 'is_active')
    inlines = [CalculatorOptionInline]
