"""Shared pytest fixtures."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.conf import settings
from django.test.utils import override_settings
from django.utils import timezone

import pytest
from model_bakery import baker

from rough_trade_calendar import models


@pytest.fixture(scope="session", autouse=True)
def set_settings():
    """Global settings for all tests."""

    with override_settings(
        # Important test settings.
        DEBUG=False,
        PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
        STATICFILES_STORAGE=settings.STATICFILES_STORAGE.replace("Manifest", ""),
        WHITENOISE_AUTOREFRESH=True,
        SECURE_SSL_REDIRECT=True,
        CACHES={
            "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
        },
    ):
        yield


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
