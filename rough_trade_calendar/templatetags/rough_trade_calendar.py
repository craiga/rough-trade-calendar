"""Template tags."""

from urllib.parse import ParseResult, urlparse

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def webcal_url(context, location):
    """Webcal URL for given location."""
    request = context["request"]
    url = reverse("location_events_calendar", kwargs={"location": location.slug})
    url = request.build_absolute_uri(url)
    parse_result = urlparse(url)
    parse_result = ParseResult("webcal", *parse_result[1:])
    return parse_result.geturl()
