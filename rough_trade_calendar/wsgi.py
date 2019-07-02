"""WSGI configuration."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rough_trade_calendar.settings")

application = get_wsgi_application()
