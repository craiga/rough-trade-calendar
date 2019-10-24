"""View tests."""

from datetime import timedelta

from django.utils import timezone

import feedparser
import pytest
import pytz
from icalendar import Calendar
from model_bakery import baker

from rough_trade_calendar import models


@pytest.mark.django_db
def test_icalendar(location, event, client):
    """Test iCalendar feed."""
    response = client.get(f"/{location.slug}/calendar", secure=True)
    assert response["Content-Type"].startswith("text/calendar")
    cal = Calendar.from_ical(response.content)
    assert location.timezone == pytz.timezone(cal.decoded("X-WR-TIMEZONE"))
    assert len(cal.subcomponents) == 1
    cal_event = cal.subcomponents[0]
    assert event.name == cal_event["SUMMARY"]
    assert event.description == cal_event["DESCRIPTION"]
    assert event.start_at.replace(microsecond=0) == cal_event.decoded("DTSTART")
    assert event.location.name == cal_event["LOCATION"]
    assert event.url == cal_event["URL"]


@pytest.mark.django_db
def test_rss(location, event, client):
    """Test RSS feed."""
    response = client.get(f"/{location.slug}/feed", secure=True)
    assert response["Content-Type"].startswith("application/rss+xml")
    feed = feedparser.parse(response.content)
    assert location.name in feed["feed"]["title"]
    assert feed["feed"]["link"].endswith(location.slug)
    assert len(feed["entries"]) == 1
    feed_event = feed["entries"][0]
    assert event.name == feed_event["title"]
    assert event.description in feed_event["summary"]
    assert event.location.name in feed_event["summary"]
    assert event.url == feed_event["link"]
    assert event.created.timetuple() == feed_event["published_parsed"]


@pytest.mark.django_db
def test_exclude_old_events(location, client):
    """Ensure old events are excluded."""
    event = baker.make(
        models.Event, location=location, start_at=timezone.now() - timedelta(days=7)
    )
    response = client.get(f"/{location.slug}", secure=True)
    assert event not in list(response.context["events"])


@pytest.mark.django_db
def test_include_yesterdays_events(location, client):
    """Ensure events less than 24 hours old are not excluded."""
    event = baker.make(
        models.Event, location=location, start_at=timezone.now() - timedelta(hours=23)
    )
    response = client.get(f"/{location.slug}", secure=True)
    assert event in list(response.context["events"])


@pytest.mark.django_db
def test_icalendar_query_count(
    location, events, client, django_assert_max_num_queries
):  # pylint: disable=unused-argument
    """Test iCalendar feed query count."""
    with django_assert_max_num_queries(2):
        client.get(f"/{location.slug}/calendar", secure=True)


@pytest.mark.django_db
def test_rss_query_count(
    location, events, client, django_assert_max_num_queries
):  # pylint: disable=unused-argument
    """Test RSS feed query count."""
    with django_assert_max_num_queries(2):
        client.get(f"/{location.slug}/feed", secure=True)
