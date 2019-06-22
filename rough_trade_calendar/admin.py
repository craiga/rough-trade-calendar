"""Admin configuration."""

from django.contrib import admin

from rough_trade_calendar import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_at", "location")
    list_display_links = list_display
    ordering = ("-start_at",)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
