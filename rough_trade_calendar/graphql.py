"""
GraphQL + Relay interface to Rough Trade Calendar data.
"""

import django_filters
import graphene
import graphene.relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from rough_trade_calendar import models


class CountConnection(graphene.Connection):
    """A connection which supports Relay's totalCount field."""

    total_count = graphene.Int()

    def resolve_total_count(self):
        return self.length  # pylint: disable=no-member

    class Meta:
        abstract = True


class EventFilterSet(django_filters.FilterSet):
    """Filter and order events by start_at."""

    start_after = django_filters.DateTimeFilter("start_at", "gt")
    start_before = django_filters.DateTimeFilter("start_at", "lt")
    order_by = django_filters.OrderingFilter(fields={"start_at": "startAt"})

    class Meta:
        model = models.Event
        fields = ["start_after", "start_before"]


class Event(DjangoObjectType):
    """An event."""

    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "url",
            "image_url",
            "start_at",
            "location",
        ]
        filterset_class = EventFilterSet
        interfaces = [graphene.relay.Node]
        connection_class = CountConnection


class Location(DjangoObjectType):
    """A location."""

    class Meta:
        model = models.Location
        fields = ["id", "name", "timezone", "events"]
        interfaces = [graphene.relay.Node]
        connection_class = CountConnection
        filter_fields = {"name": ["exact", "contains"]}


class Query(graphene.ObjectType):
    all_locations = DjangoFilterConnectionField(Location, description="All locations.")


schema = graphene.Schema(query=Query)
