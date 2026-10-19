from django.contrib import admin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_autoslug import AutoSlugAdminMixin
from apps.core.admin_site_content_widgets import CmsAdminTinyMCEWidget
from apps.core.admin_translation_forms import TranslationSyncModelForm
from apps.core.cms_i18n import lang_field_set, lang_fields

from .models import BlogFAQItem, BlogPost, FAQItem


_FAQ_TINYMCE = lang_field_set('answer')
_BODY_TINYMCE = lang_field_set('body', 'excerpt')


@admin.register(FAQItem)
class FAQItemAdmin(ModelAdmin):
    list_display = ('question', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    search_fields = ('question', 'answer')
    ordering_field = 'sort_order'
    fields = (*lang_fields('question', 'answer'), 'sort_order', 'is_active')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in _FAQ_TINYMCE:
            kwargs['widget'] = CmsAdminTinyMCEWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class BlogFAQItemInline(TabularInline):
    model = BlogFAQItem
    extra = 1
    ordering_field = 'sort_order'
    fields = (*lang_fields('question', 'answer'), 'sort_order')

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
        *lang_fields('title', 'excerpt', 'body'),
        'cover',
        *lang_fields('cover_alt', 'meta_title', 'meta_description'),
        'published_at', 'is_published', 'sort_order',
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in _BODY_TINYMCE:
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
