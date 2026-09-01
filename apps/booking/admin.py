from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

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
    list_filter = ('service', 'is_active')


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'slot', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email')
