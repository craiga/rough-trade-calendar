from rough_trade_calendar import models


class EventDjangoPipeline(object):
    def process_item(self, item, spider):
        try:
            event = models.Event.objects.get(url=item["url"])
            item._instance = event

        except models.Event.DoesNotExist:
            pass

        item.save()

        return item
