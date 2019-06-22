import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import scrapy
import scrapy_djangoitem
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from rough_trade_calendar import models


class Event(scrapy_djangoitem.DjangoItem):
    django_model = models.Event


class EventsSpider(scrapy.Spider):
    name = "rough_trade_events"

    def start_requests(self):
        now = datetime.now()
        for loc in models.Location.objects.all():
            for month_num in range(0, 6):
                date = now + relativedelta(months=month_num)
                url = "/".join([loc.events_url, str(date.year), str(date.month)])
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # TODO: Move into model manager?
        url = re.sub(r"/\d{4}/\d{1,2}$", "", response.url)
        loc = models.Location.objects.get(events_url=url)

        for event in response.xpath("//div[contains(@class, 'event')]"):
            start_at = parse(event.xpath(".//*[@class='text-sm']/text()").get())
            start_at = loc.timezone.localize(start_at)
            event = Event(
                name=event.xpath(".//h2/a/text()").get(),
                description=event.get(),
                url=urljoin(response.url, event.xpath(".//a/@href").get()),
                image_url=urljoin(response.url, event.xpath(".//img/@src").get()),
                start_at=start_at,
                location=loc,
            )
            yield event
