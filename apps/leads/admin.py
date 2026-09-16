from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.core.admin_filters import (
    RsBooleanDropdownFilter,
    RsChoicesDropdownFilter,
    dropdown_filter_options,
)

from .models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('kind', 'name', 'phone', 'email', 'company', 'is_processed', 'created_at')
    list_filter = (
        ('kind', RsChoicesDropdownFilter),
        ('is_processed', RsBooleanDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'kind', 'is_processed',
        labels={'is_processed': 'Оброблено'},
    )
    search_fields = ('name', 'phone', 'email', 'company')
