"""View tests."""

import pytest
import pytz
from icalendar import Calendar


@pytest.mark.django_db
def test_icalendar(location, event, client):
    """Test iCalendar feed."""
    response = client.get(f"/{location.slug}/calendar")
    assert response["Content-Type"].startswith("text/calendar")
    cal = Calendar.from_ical(response.content)
    assert location.timezone == pytz.timezone(cal.decoded("X-WR-TIMEZONE"))
    assert len(cal.subcomponents) == 1
    cal_event = cal.subcomponents[0]
    assert event.name == cal_event["SUMMARY"]
    assert event.description == cal_event["DESCRIPTION"]
    assert event.start_at.replace(microsecond=0) == cal_event.decoded("DTSTAMP")
    assert event.start_at.replace(microsecond=0) == cal_event.decoded("DTSTART")
    assert event.location.name == cal_event["LOCATION"]
    assert event.url == cal_event["URL"]


@pytest.mark.django_db
def test_location(location, client):
    """Test location view."""
    response = client.get(f"/{location.slug}")
    assert response.context["cal_url"] == f"http://testserver/{location.slug}/calendar"
    assert (
        response.context["webcal_url"]
        == f"webcal://testserver/{location.slug}/calendar"
    )
