"""Shared pytest fixtures."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.utils import timezone

import pytest
from model_mommy import mommy

from rough_trade_calendar import models


@pytest.fixture
def location():
    return mommy.make(models.Location)


@pytest.fixture
def event(location):
    return mommy.make(
        models.Event, location=location, start_at=timezone.now() + timedelta(days=3)
    )
