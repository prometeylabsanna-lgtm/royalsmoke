from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_filters import (
    RsBooleanDropdownFilter,
    RsChoicesDropdownFilter,
    RsRelatedDropdownFilter,
    dropdown_filter_options,
)

from .models import Booking, BookingService, BookingSlot


class BookingSlotInline(TabularInline):
    model = BookingSlot
    extra = 1


@admin.register(BookingService)
class BookingServiceAdmin(ModelAdmin):
    list_display = ('title', 'kind', 'duration_minutes', 'capacity', 'is_active')
    inlines = [BookingSlotInline]


@admin.register(BookingSlot)
class BookingSlotAdmin(ModelAdmin):
    list_display = ('service', 'starts_at', 'ends_at', 'capacity', 'is_active')
    list_filter = (
        ('service', RsRelatedDropdownFilter),
        ('is_active', RsBooleanDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'service', 'is_active',
        labels={'is_active': 'Активність'},
    )


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'slot', 'status', 'created_at')
    list_filter = (
        ('status', RsChoicesDropdownFilter),
        ('slot__service', RsRelatedDropdownFilter),
    )
    list_filter_sheet = False
    list_filter_options = dropdown_filter_options(
        'status', 'slot__service',
        labels={'slot__service': 'Послуга'},
    )
    list_editable = ('status',)
    search_fields = ('name', 'phone', 'email')
    date_hierarchy = 'created_at'
