from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.core.admin_chrome_style import ChromeStyleAdmin  # noqa: F401
from apps.core.admin_page_style import PageStyleAdmin  # noqa: F401
from apps.core.admin_site_content_proxies import register_site_content_section_admins  # noqa: F401
from apps.core.models import CurrencyRate, SiteSettings
from apps.core.validation.admin_forms import SiteSettingsAdminForm


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    form = SiteSettingsAdminForm
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


@admin.register(CurrencyRate)
class CurrencyRateAdmin(ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'uah_per_unit', 'sort_order')
    list_display_links = ('code',)
    list_editable = ('uah_per_unit', 'sort_order')
    search_fields = ('code', 'name')
    ordering = ('sort_order', 'code')
