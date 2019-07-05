"""Views."""

from datetime import timedelta

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
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
        return models.Event.objects.filter(
            location=self.location, start_at__gte=timezone.now() - timedelta(days=1)
        ).order_by("start_at")

    def get_context_data(self, *args, **kwargs):  # pylint: disable=arguments-differ
        context = super().get_context_data(*args, **kwargs)
        context["location"] = self.location
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
        return models.Event.objects.filter(
            location=location, start_at__gte=timezone.now() - timedelta(days=1)
        )

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


class LocationEventsFeed(Feed):
    """Location RSS feed."""

    def get_object(self, request, location):  # pylint: disable=arguments-differ
        return models.Location.objects.get(slug=location)

    def link(self, location):
        return reverse("location_events", kwargs={"location": location.slug})

    def title(self, location):
        return location.name

    def items(self, location):
        return models.Event.objects.filter(
            location=location, start_at__gte=timezone.now() - timedelta(days=1)
        ).order_by("created")

    def item_link(self, item):
        return item.url

    def item_description(self, item):
        return f"{item.description}\n{item.location} at {item.start_at}"

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.modified
