from django.contrib import admin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_autoslug import AutoSlugAdminMixin
from apps.core.admin_site_content_widgets import CmsAdminTinyMCEWidget
from apps.core.admin_translation_forms import TranslationSyncModelForm

from .models import BlogFAQItem, BlogPost, FAQItem


_FAQ_TINYMCE = {
    'answer', 'answer_uk', 'answer_en', 'answer_zh_hans',
}
_BODY_TINYMCE = {
    'body', 'body_uk', 'body_en', 'body_zh_hans',
    'excerpt', 'excerpt_uk', 'excerpt_en', 'excerpt_zh_hans',
}


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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in _FAQ_TINYMCE:
            kwargs['widget'] = CmsAdminTinyMCEWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class BlogFAQItemInline(TabularInline):
    model = BlogFAQItem
    extra = 1
    ordering_field = 'sort_order'
    fields = (
        'question_uk', 'question_en', 'question_zh_hans',
        'answer_uk', 'answer_en', 'answer_zh_hans',
        'sort_order',
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in _FAQ_TINYMCE:
            kwargs['widget'] = CmsAdminTinyMCEWidget(mce_attrs={'height': 200})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class BlogPostAdminForm(TranslationSyncModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogPost)
class BlogPostAdmin(AutoSlugAdminMixin, ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'slug', 'is_published', 'published_at', 'sort_order')
    list_editable = ('is_published', 'sort_order')
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'slug')
    prepopulated_fields = {'slug': ('title_uk',)}
    ordering_field = 'sort_order'
    date_hierarchy = 'published_at'
    inlines = (BlogFAQItemInline,)
    fields = (
        'slug',
        'title_uk', 'title_en', 'title_zh_hans',
        'excerpt_uk', 'excerpt_en', 'excerpt_zh_hans',
        'body_uk', 'body_en', 'body_zh_hans',
        'cover',
        'cover_alt_uk', 'cover_alt_en', 'cover_alt_zh_hans',
        'meta_title_uk', 'meta_title_en', 'meta_title_zh_hans',
        'meta_description_uk', 'meta_description_en', 'meta_description_zh_hans',
        'published_at', 'is_published', 'sort_order',
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in _BODY_TINYMCE:
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
