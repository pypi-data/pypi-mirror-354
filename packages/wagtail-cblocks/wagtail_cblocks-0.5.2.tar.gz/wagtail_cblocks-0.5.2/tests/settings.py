import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
VAR_DIR = Path(__file__).parent / "var"

# GENERAL

DEBUG = True if os.environ.get("INTERACTIVE", "0") == "1" else False

SECRET_KEY = "not-a-secure-key"  # noqa: S105

ALLOWED_HOSTS = ["localhost", "testserver"]

# INTERNATIONALIZATION

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_TZ = True

# DATABASE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "sqlite.db"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLS

ROOT_URLCONF = "tests.urls"

# APP CONFIGURATION

INSTALLED_APPS = [
    "wagtail_cblocks",
    "tests",
    # wagtail
    "wagtail.sites",
    "wagtail.users",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# PASSWORDS

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# MIDDLEWARE

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# STATIC

STATIC_ROOT = VAR_DIR / "static"

STATIC_URL = "/static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA

MEDIA_ROOT = VAR_DIR / "media"

MEDIA_URL = "/media/"

# TEMPLATES

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
        },
    },
]

# CACHES

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# WAGTAIL

WAGTAILADMIN_BASE_URL = "http://testserver"

WAGTAIL_SITE_NAME = "wagtail-cblocks test"
