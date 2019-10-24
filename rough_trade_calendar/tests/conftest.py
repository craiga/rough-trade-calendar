"""Shared pytest fixtures."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.utils import timezone

import pytest
from model_bakery import baker

from rough_trade_calendar import models


@pytest.fixture
def location():
    return baker.make(models.Location)


@pytest.fixture
def event(location):
    return baker.make(
        models.Event, location=location, start_at=timezone.now() + timedelta(days=3)
    )


@pytest.fixture
def events(location):
    return baker.make(
        models.Event,
        location=location,
        start_at=timezone.now() + timedelta(days=3),
        _quantity=5,
    )
