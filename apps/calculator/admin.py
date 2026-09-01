from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import CalculatorOption, CalculatorQuestion


class CalculatorOptionInline(TabularInline):
    model = CalculatorOption
    extra = 2


@admin.register(CalculatorQuestion)
class CalculatorQuestionAdmin(ModelAdmin):
    list_display = ('title', 'step_key', 'sort_order', 'is_active')
    inlines = [CalculatorOptionInline]
