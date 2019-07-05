"""URL Configuration."""

from django.contrib import admin
from django.urls import path

from rough_trade_calendar import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "<location>/calendar",
        views.LocationEventsCalendar(),
        name="location_events_calendar",
    ),
    path("<location>/feed", views.LocationEventsFeed(), name="location_events_feed"),
    path("<location>", views.LocationEvents.as_view(), name="location_events"),
    path("", views.Locations.as_view(), name="locations"),
]
