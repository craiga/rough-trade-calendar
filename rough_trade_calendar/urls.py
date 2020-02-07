"""URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

import debug_toolbar
from csp.decorators import csp_exempt
from graphene_django.views import GraphQLView

from rough_trade_calendar import views

urlpatterns = [
    path("datadatadata/", admin.site.urls),
    path("graphql", csp_exempt(csrf_exempt(GraphQLView.as_view(graphiql=True)))),
    path(
        "<location>/calendar",
        views.LocationEventsCalendar(),
        name="location_events_calendar",
    ),
    path("<location>/feed", views.LocationEventsFeed(), name="location_events_feed"),
    path("<location>", views.LocationEvents.as_view(), name="location_events"),
    path("", views.Locations.as_view(), name="locations"),
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
