from django.utils.translation import gettext_lazy as _t

from pathlib import Path
from decouple import config
from datetime import timedelta
import os
import sys

# Extract Python version
python_version = sys.version_info
version_float = float(f"{python_version.major}.{python_version.minor}")

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the application
SECRET_KEY = config("SECRET_KEY")

# Debug mode and allowed hosts
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="*", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "corsheaders",
    "rest_framework",
    "django_filters",
    "modeltranslation",
    "import_export",
    # local apps
    "app_user",
    "app_doctor",
    "app_reservation",
    "app_settings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # CORS headers
    "corsheaders.middleware.CorsMiddleware",
    # Locale middleware
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# Database configuration
SQL_LITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if config("USE_MYSQL", default=False, cast=bool):
    MYSQL_DATABASE = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_NAME"),
        "USER": config("MYSQL_USER"),
        "PASSWORD": config("MYSQL_PASS"),
        "HOST": config("MYSQL_HOST"),
        "PORT": config("MYSQL_PORT", cast=int),
    }

if config("USE_POSTGRES", default=False, cast=bool):
    POSTGRES_SQL_DATABASE = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_NAME"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASS"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", cast=int),
    }


def get_default_database(default_database=config("DEFAULT_DATABASE_NAME", default="")):
    """
    Return the appropriate database configuration based on the default database type.
    Supports MySQL, PostgreSQL, and SQLite.
    """
    if version_float >= 3.10:
        match default_database.upper():
            case "MYSQL":
                return MYSQL_DATABASE
            case "POSTGRESQL":
                return POSTGRES_SQL_DATABASE
            case _:
                return SQL_LITE_DATABASE
    else:
        return (
            MYSQL_DATABASE
            if default_database.upper() == "MYSQL"
            else POSTGRES_SQL_DATABASE
            if default_database.upper() == "POSTGRESQL"
            else SQL_LITE_DATABASE
        )


DATABASES = {"default": get_default_database()}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Default auto field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "app_user.User"

# Static files configuration
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Media files configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Internationalization settings
LANGUAGES = [
    ("en", _t("English")),
    ("fa", _t("Persian")),
]
LANGUAGE_CODE = "fa"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

# Data masking
FERNET_KEY = config("FERNET_KEY")

# ___django rest framework settings___ #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# __django multi language settings__ #
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

MEDIANA_API_KEY = config("MEDIANA_API_KEY")
SMS_SEND_CODE = config("SMS_SEND_CODE")
SMS_SEND_INFO = config("SMS_SEND_INFO")

# Request API options
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = config(
    "CORS_ORIGIN_REGEX_WHITELIST",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="http://localhost:8000",
)

# Django REST Framework SimpleJWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        hours=config("ACCESS_TOKEN_LIFETIME", default=1, cast=int)
    ),
}

# Custom settings
DATE_INPUT_FORMAT = "%Y-%m-%d"
TIME_INPUT_FORMAT = "%H:%M:%S"
MAXIMUM_COUNT_TRY_WRONG_OTP_CODE = 5
