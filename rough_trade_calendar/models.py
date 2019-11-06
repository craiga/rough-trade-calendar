"""Models."""

import re

from django.db import models

from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField


class LocationManager(models.Manager):
    """Location manager."""

    def get_by_events_url(self, events_url):
        events_url = re.sub(r"/\d{4}/\d{1,2}$", "", events_url)
        return self.get(events_url=events_url)


class Location(models.Model):
    """Location."""

    name = models.TextField()
    slug = models.SlugField()
    events_url = models.URLField()
    timezone = TimeZoneField()

    objects = LocationManager()

    def __str__(self):
        return self.name


class Event(TimeStampedModel):
    """Event."""

    name = models.TextField()
    description = models.TextField()
    url = models.URLField(unique=True)
    image_url = models.URLField()
    youtube_id = models.TextField()
    detail_html = models.TextField()
    start_at = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return self.name
