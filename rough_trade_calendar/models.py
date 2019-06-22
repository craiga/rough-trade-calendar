from django.db import models

import pytz
from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField


class Location(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    events_url = models.URLField()
    timezone = TimeZoneField()

    def __str__(self):
        return self.name


class Event(TimeStampedModel):
    name = models.TextField()
    description = models.TextField()
    url = models.URLField(unique=True)
    image_url = models.URLField()
    start_at = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return self.name
