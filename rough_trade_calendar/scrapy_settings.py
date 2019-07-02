"""Scrapy settings."""

import os

from django.core.wsgi import get_wsgi_application

# Configure and start required Django things.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rough_trade_calendar.settings")
app = get_wsgi_application()


SPIDER_MODULES = ["rough_trade_calendar.spiders"]

ITEM_PIPELINES = {"rough_trade_calendar.pipelines.EventDjangoPipeline": 300}
