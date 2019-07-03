"""Scrapy settings."""

import os

from django.core.wsgi import get_wsgi_application

import sentry_sdk

sentry_sdk.init()


# Configure and start required Django things.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rough_trade_calendar.settings")
app = get_wsgi_application()


SPIDER_MODULES = ["rough_trade_calendar.spiders"]

ITEM_PIPELINES = {"rough_trade_calendar.pipelines.EventDjangoPipeline": 300}

EXTENSIONS = {
    # https://github.com/llonchj/scrapy-sentry
    "scrapy_sentry.extensions.Errors": 10
}
