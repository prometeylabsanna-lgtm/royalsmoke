from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from apps.core.admin_site_content import site_content_section_view
from apps.core.models import (
    HomeAboutSettings,
    HomeCategoriesSettings,
    HomeHeroSettings,
    HomeNewSettings,
    HomeServiceSettings,
    HomeTopSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteSettings,
)


class SingletonSettingsAdmin(ModelAdmin):
    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        url_name = f'admin:core_{self.model._meta.model_name}_change'
        return HttpResponseRedirect(reverse(url_name, args=[obj.pk]))


class SiteContentSectionAdmin(SingletonSettingsAdmin):
    page_slug: str = ''
    section_slug: str = ''

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return site_content_section_view(
            request, self.page_slug, self.section_slug, model_admin=self,
        )


_SECTION_MODELS = (
    (HomeHeroSettings, 'home', 'hero'),
    (HomeCategoriesSettings, 'home', 'categories'),
    (HomeTopSettings, 'home', 'top'),
    (HomeNewSettings, 'home', 'new'),
    (HomeAboutSettings, 'home', 'about'),
    (HomeServiceSettings, 'home', 'service'),
    (SiteHeaderSettings, 'site', 'header'),
    (SiteFooterSettings, 'site', 'footer'),
)


def register_site_content_section_admins() -> None:
    for model, page_slug, section_slug in _SECTION_MODELS:
        class SectionAdmin(SiteContentSectionAdmin):
            pass

        SectionAdmin.__name__ = f'{model.__name__}Admin'
        SectionAdmin.page_slug = page_slug
        SectionAdmin.section_slug = section_slug
        admin.site.register(model, SectionAdmin)


register_site_content_section_admins()
