"""Template tags tests."""

# pylint: disable=redefined-outer-name

import pytest

from rough_trade_calendar.templatetags import rough_trade_calendar


@pytest.fixture
def context(rf):
    return {"request": rf.get("http://testserver/some/page")}


@pytest.mark.django_db
def test_webcal_url(context, location):
    """Test webcal URL."""
    assert (
        rough_trade_calendar.webcal_url(context, location)
        == f"webcal://testserver/{location.slug}/calendar"
    )
