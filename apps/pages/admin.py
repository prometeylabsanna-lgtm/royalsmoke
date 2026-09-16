from django.contrib import admin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import FAQItem, LegalDocument


@admin.register(FAQItem)
class FAQItemAdmin(ModelAdmin):
    list_display = ('question', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    search_fields = ('question', 'answer')
    ordering_field = 'sort_order'
    fields = (
        'question_uk', 'question_en', 'question_zh_hans',
        'answer_uk', 'answer_en', 'answer_zh_hans',
        'sort_order', 'is_active',
    )


@admin.register(LegalDocument)
class LegalDocumentAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('title_uk',)}
    ordering_field = 'sort_order'
    fields = (
        'slug',
        'title_uk', 'title_en', 'title_zh_hans',
        'body_uk', 'body_en', 'body_zh_hans',
        'sort_order', 'is_active',
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in {'body_uk', 'body_en', 'body_zh_hans'}:
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
