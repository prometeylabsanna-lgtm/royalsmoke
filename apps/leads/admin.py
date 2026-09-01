from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('kind', 'name', 'phone', 'email', 'company', 'is_processed', 'created_at')
    list_filter = ('kind', 'is_processed')
    search_fields = ('name', 'phone', 'email', 'company')
