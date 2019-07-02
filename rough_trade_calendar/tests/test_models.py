"""Model tests."""

from urllib.parse import urljoin

import pytest

from rough_trade_calendar import models


@pytest.mark.django_db
def test_location_get_by_events_url(location):
    """Test retrieving location by event page URL."""
    for url in [location.events_url, location.events_url + "/1234/5"]:
        assert location == models.Location.objects.get_by_events_url(url)

    for url in ["http://craiga.id.au", urljoin(location.events_url, "/some/junk")]:
        with pytest.raises(models.Location.DoesNotExist):
            models.Location.objects.get_by_events_url(url)
