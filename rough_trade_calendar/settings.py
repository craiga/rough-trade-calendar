"""Django settings."""

import os
import re

import dj_database_url
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
    "django.middleware.security.SecurityMiddleware",
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
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"


# Ignore 404s
# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-IGNORABLE_404_URLS

IGNORABLE_404_URLS = [re.compile(r"^/phpmyadmin/"), re.compile(r"\.php$")]

# Security
# https://docs.djangoproject.com/en/2.2/topics/security/

SECURE_HSTS_SECONDS = 0 if DEBUG else 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"


# Internal IPs (required for Django Debug Toolbar)
# https://docs.djangoproject.com/en/2.2/ref/settings/#internal-ips

INTERNAL_IPS = os.environ.get("INTERNAL_IPS", "127.0.0.1").split(" ")


# Configure Django App for Heroku.
django_heroku.settings(locals())


if os.environ.get("DATABASE_NO_SSL_REQUIRE"):
    DATABASES["default"] = dj_database_url.config(ssl_require=False)
