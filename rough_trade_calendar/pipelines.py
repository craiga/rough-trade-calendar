from rough_trade_calendar import models


class EventDjangoPipeline(object):
    def process_item(self, item, spider):
        try:
            event = models.Event.objects.get(url=item["url"])

            # Event already exists.
            event_id = event.id
            event = item.save(commit=False)
            event.id = event_id

        except models.Event.DoesNotExist:
            pass

        item.save()

        return item
