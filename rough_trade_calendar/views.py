"""Views."""

from datetime import timedelta
from urllib.parse import ParseResult, urlparse

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from django_ical.views import ICalFeed

from rough_trade_calendar import models


class Locations(ListView):
    """Location listing view."""

    model = models.Location
    context_object_name = "locations"


class LocationEvents(ListView):
    """Events listing view."""

    model = models.Event
    context_object_name = "events"

    def get_queryset(self):
        # pylint: disable=attribute-defined-outside-init
        self.location = get_object_or_404(models.Location, slug=self.kwargs["location"])
        return models.Event.objects.filter(location=self.location).order_by("start_at")

    def build_cal_url(self):
        url = reverse(
            "location_events_calendar", kwargs={"location": self.location.slug}
        )
        return self.request.build_absolute_uri(url)

    def build_webcal_url(self):
        parse_result = urlparse(self.build_cal_url())
        parse_result = ParseResult("webcal", *parse_result[1:])
        return parse_result.geturl()

    def get_context_data(self, *args, **kwargs):  # pylint: disable=arguments-differ
        context = super().get_context_data(*args, **kwargs)
        context["location"] = self.location
        context["cal_url"] = self.build_cal_url()
        context["webcal_url"] = self.build_webcal_url()
        return context


# pylint: disable=no-self-use
class LocationEventsCalendar(ICalFeed):
    """Location iCal feed."""

    def get_object(self, request, location):  # pylint: disable=arguments-differ
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
