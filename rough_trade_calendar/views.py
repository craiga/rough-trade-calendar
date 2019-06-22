from datetime import timedelta

from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from django_ical.views import ICalFeed

from rough_trade_calendar import models


class Locations(ListView):
    model = models.Location
    context_object_name = "locations"


class LocationEvents(ListView):
    model = models.Event
    context_object_name = "events"

    def get_queryset(self):
        self.location = get_object_or_404(models.Location, slug=self.kwargs["location"])
        return models.Event.objects.filter(location=self.location).order_by("start_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["location"] = self.location
        return context


class LocationEventsCalendar(ICalFeed):

    def get_object(self, request, location):
        return models.Location.objects.get(slug=location)

    def title(self, location):
        return f"Rough Trade {location.name} Events"

    def timezone(self, location):
        return location.timezone

    def items(self, location):
        return models.Event.objects.filter(location=location)

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_at

    def item_end_datetime(self, item):
        return item.start_at + timedelta(hours=2)

    def item_link(self, item):
        return item.url

    def item_location(self, item):
        return item.location.name
