"""Events spider tests."""

# pylint: disable=redefined-outer-name

from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pytest
from scrapy.http import TextResponse

from rough_trade_calendar import spiders


@pytest.fixture
def html():
    """
    Returns HTML retrieved with the following command:

        curl https://www.roughtrade.com/events/store/rough-trade-east \
            > rough_trade_calendar/tests/test_data/events.html

    Note that the first event in this file should be changed to match the data in these
    tests.
    """
    this_filename = globals()["__file__"]
    path = Path(this_filename).parents[0] / Path("test_data/events.html")
    return path.read_text()


@pytest.fixture
def response(location, html):
    return TextResponse(f"{location.events_url}/1978/3", body=html, encoding="utf-8")


@pytest.fixture
def empty_html():
    """
    Returns HTML retrieved with the following command:

        curl https://www.roughtrade.com/events/store/rough-trade-east/2019/10 \
            > rough_trade_calendar/tests/test_data/events_empty.html
    """
    this_filename = globals()["__file__"]
    path = Path(this_filename).parents[0] / Path("test_data/events_empty.html")
    return path.read_text()


@pytest.fixture
def empty_response(location, empty_html):
    return TextResponse(location.events_url, body=empty_html, encoding="utf-8")


@pytest.mark.django_db
def test_spider_parse(response, location):
    """Test that spider parses HTML."""
    spider = spiders.EventsSpider()
    event_items = list(spider.parse(response, date=datetime(1978, 1, 1)))
    assert len(event_items) == 11

    event_item = event_items[0]
    assert event_item["name"] == "Twenty Minute Bass Solo"
    assert event_item["description"] == "The search for the elusive brown note. 💩"
    assert event_item["url"] == urljoin(location.events_url, "/events/bass-solo")
    assert (
        event_item["image_url"]
        == "https://gravatar.com/avatar/b593bb966ccde8a4a4fbdc32d2aafb6f.jpeg"
    )
    assert event_item["start_at"] == location.timezone.localize(
        datetime(1978, 3, 31, 12, 34, 0)
    )
    assert event_item["location"] == location

    event_item = event_items[1]
    assert event_item["name"] == "No Description"


@pytest.mark.django_db
def test_spider_parse_empty(empty_response):
    """Test that spider parses HTML."""
    spider = spiders.EventsSpider()
    event_items = list(spider.parse(empty_response, date=datetime(1978, 1, 1)))
    assert event_items == []
