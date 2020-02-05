"""Django settings."""

import ipaddress
import os
import re

import dj_database_url
import django_feature_policy
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(integrations=[DjangoIntegration()])


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "placeholder")

DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = ["*.herokuapp.com", "localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "timezone_field",
    "debug_toolbar",
    "rough_trade_calendar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "enforce_host.EnforceHostMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rough_trade_calendar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "string_if_invalid": "ERROR: '%s' is invalid." if DEBUG else "",
        },
    }
]

WSGI_APPLICATION = "rough_trade_calendar.wsgi.application"


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = "/static/"


# Ignore 404s
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-IGNORABLE_404_URLS

IGNORABLE_404_URLS = [re.compile(r"^/phpmyadmin/"), re.compile(r"\.php$")]

# Security
# https://docs.djangoproject.com/en/stable/topics/security/

SECURE_HSTS_SECONDS = 0 if DEBUG else 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"


# Internal IPs (required for Django Debug Toolbar)
# https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips


class IPv4List(list):
    """IPv4 addresses from CIDR."""

    def __init__(self, cidr):
        super().__init__()
        self.network = ipaddress.IPv4Network(cidr)

    def __contains__(self, ip):
        return ipaddress.IPv4Address(ip) in self.network


INTERNAL_IPS = IPv4List(os.environ.get("INTERNAL_IP_CIDR", "127.0.0.1/32"))


# Content Security Policy
# https://django-csp.readthedocs.io/en/stable/configuration.html

CSP_STYLE_SRC = ["'self'", "unpkg.com"]
CSP_IMG_SRC = ["'self'", "images.roughtrade.com", "https://collect.usefathom.com"]
CSP_SCRIPT_SRC = ["'unsafe-inline'", "https://cdn.usefathom.com"]
CSP_REPORT_URI = os.environ.get("CSP_REPORT_URI", None)

if DEBUG:
    # CSP requirements for Django Debug Toolbar.
    CSP_SCRIPT_SRC += ["'self'"]


# Feature policy
# https://github.com/adamchainz/django-feature-policy#setting

FEATURE_POLICY = {
    feature_name: "none" for feature_name in django_feature_policy.FEATURE_NAMES
}


# Enforce Host
# https://github.com/dabapps/django-enforce-host

ENFORCE_HOST = os.environ.get("CANONICAL_HOST")


# Configure Django App for Heroku.
django_heroku.settings(locals())


if os.environ.get("DATABASE_NO_SSL_REQUIRE"):
    DATABASES["default"] = dj_database_url.config(ssl_require=False)
