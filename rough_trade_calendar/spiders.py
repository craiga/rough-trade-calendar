"""Scrapy spiders."""

from datetime import datetime
from urllib.parse import urljoin

import scrapy
import scrapy_djangoitem
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from rough_trade_calendar import models


class Event(scrapy_djangoitem.DjangoItem):
    django_model = models.Event


class EventsSpider(scrapy.Spider):
    """Events spider."""

    name = "rough_trade_events"

    def start_requests(self):
        now = datetime.now()
        for loc in models.Location.objects.all():
            for month_num in range(0, 6):
                date = now + relativedelta(months=month_num)
                url = "/".join([loc.events_url, str(date.year), str(date.month)])
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        loc = models.Location.objects.get_by_events_url(response.url)

        for event in response.xpath("//div[contains(@class, 'event-same-height')]"):
            start_at = parse(event.xpath(".//*[@class='text-sm']/text()").get())
            start_at = loc.timezone.localize(start_at)

            description = event.xpath(".//div[contains(@class, 'f-n')]/text()").get()
            if description is None:
                description = ""

            event = Event(
                name=event.xpath(".//h2/a/text()").get(),
                description=description,
                url=urljoin(response.url, event.xpath(".//a/@href").get()),
                image_url=urljoin(response.url, event.xpath(".//img/@src").get()),
                start_at=start_at,
                location=loc,
            )

            yield event
