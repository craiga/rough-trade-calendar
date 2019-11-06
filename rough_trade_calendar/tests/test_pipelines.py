"""Scrapy pipeline tests."""

# pylint: disable=no-member, redefined-outer-name

import faker
import pytest

from rough_trade_calendar import models, pipelines, spiders

fake = faker.Faker()


@pytest.fixture
def new_event_item(location):
    return spiders.Event(
        name=fake.sentence(),
        description=fake.sentence(),
        url=fake.uri_path(),
        image_url=fake.image_url(),
        start_at=fake.date_time(),
        location=location,
    )


@pytest.fixture
def existing_event_item(location, event):
    return spiders.Event(
        name=fake.sentence(),
        description=fake.sentence(),
        url=event.url,
        image_url=fake.image_url(),
        start_at=fake.date_time(),
        location=location,
    )


@pytest.fixture
def detail_event_item(event):
    return spiders.Event(
        url=event.url, youtube_id=fake.pystr(), detail_html=fake.pystr()
    )


@pytest.mark.django_db
def test_pipeline_update_create(new_event_item):
    """Test that items are created by the pipeline."""
    pipeline = pipelines.EventDjangoPipeline()
    assert not models.Event.objects.filter(url=new_event_item["url"]).exists()
    pipeline.process_item(new_event_item, None)
    assert models.Event.objects.filter(url=new_event_item["url"]).exists()


@pytest.mark.django_db
def test_pipeline_update(existing_event_item, event):
    """Test that items are updated by the pipeline."""
    initial_created = event.created
    pipeline = pipelines.EventDjangoPipeline()
    assert not event.name == existing_event_item["name"]
    pipeline.process_item(existing_event_item, None)
    event.refresh_from_db()
    assert event.name == existing_event_item["name"]
    assert event.created == initial_created


@pytest.mark.django_db
def test_pipeline_update_with_detail(detail_event_item, event):
    """Test that items are updated with details."""
    initial_created = event.created
    pipeline = pipelines.EventDjangoPipeline()
    assert not event.detail_html == detail_event_item["detail_html"]
    pipeline.process_item(detail_event_item, None)
    event.refresh_from_db()
    assert event.detail_html == detail_event_item["detail_html"]
    assert event.created == initial_created
