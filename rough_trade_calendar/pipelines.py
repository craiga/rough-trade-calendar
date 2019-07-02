"""Scrapy pipelines."""

from rough_trade_calendar import models


class EventDjangoPipeline:
    """Save events to Django models."""

    def process_item(
        self, item, spider
    ):  # pylint: disable=no-self-use, unused-argument
        """Process item."""
        try:
            event = models.Event.objects.get(url=item["url"])
            item["created"] = event.created
            event_id = event.id
            event = item.save(commit=False)
            event.id = event_id

        except models.Event.DoesNotExist:
            pass

        item.save()
        return item
