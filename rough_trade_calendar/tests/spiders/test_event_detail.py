"""Event detail spider tests."""

# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest
from scrapy.http import TextResponse

from rough_trade_calendar import models, spiders


@pytest.fixture
def html():
    """
    Returns HTML of an event detail page.

    The data in this file should match what's in the tests below.
    """
    this_filename = globals()["__file__"]
    path = Path(this_filename).parents[0] / Path("test_data/event.html")
    return path.read_text()


@pytest.fixture
def no_youtube_html():
    """
    Returns HTML of an event detail page.

    The data in this file should match what's in the tests below.
    """
    this_filename = globals()["__file__"]
    path = Path(this_filename).parents[0] / Path("test_data/event_no_youtube.html")
    return path.read_text()


@pytest.fixture
def response(event, html):
    return TextResponse(event.url, body=html, encoding="utf-8")


@pytest.fixture
def no_youtube_response(event, no_youtube_html):
    return TextResponse(event.url, body=no_youtube_html, encoding="utf-8")


@pytest.fixture
def response_404(event):
    return TextResponse(event.url, status=404)


@pytest.mark.django_db
def test_spider_parse(response):
    """Test that spider parses HTML."""
    spider = spiders.EventDetailSpider()
    event_items = list(spider.parse(response))
    assert len(event_items) == 1
    event_item = event_items[0]
    assert event_item["youtube_id"] == "cool-video"
    assert "Hey dudes!" in event_item["detail_html"]


@pytest.mark.django_db
def test_no_youtube(no_youtube_response):
    """Test that spider parses HTML without a YouTube link."""
    spider = spiders.EventDetailSpider()
    event_items = list(spider.parse(no_youtube_response))
    assert len(event_items) == 1
    event_item = event_items[0]
    assert event_item["youtube_id"] == ""


@pytest.mark.django_db
def test_spider_404(response_404, event):
    """Test that spider deletes events which no longer exist."""
    spider = spiders.EventDetailSpider()
    event_items = list(spider.parse(response_404))
    assert len(event_items) == 0
    with pytest.raises(models.Event.DoesNotExist):
        event.refresh_from_db()
