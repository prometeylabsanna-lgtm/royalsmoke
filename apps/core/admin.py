from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_site_content_proxies import register_site_content_section_admins  # noqa: F401
from apps.core.models import HeroSlide, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ('site_name', 'phone', 'email')

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(reverse('admin:core_sitesettings_change', args=[obj.pk]))


class HeroSlideInline(TabularInline):
    model = HeroSlide
    extra = 0


# HeroSlide not registered as standalone ModelAdmin (managed via CMS hero section)
