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

            # Copy data not specified in the item from the existing model instance.
            for field in event._meta.fields:
                if field.name == "id":  # don't copy the ID!
                    continue

                if field.name not in item:
                    item[field.name] = getattr(event, field.name)

            event_id = event.id
            event = item.save(commit=False)
            event.id = event_id

        except models.Event.DoesNotExist:
            pass

        item.save()
        return item
