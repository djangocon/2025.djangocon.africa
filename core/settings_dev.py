import dj_database_url
import os
from .settings_base import *  # noqa: F403

SECRET_KEY = "not really a secret"
DEBUG = True
BASE_URL = "localhost"
ALLOWED_HOSTS = []

MIDDLEWARE += [  # noqa: F405
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INSTALLED_APPS += [  # noqa: F405
    "django_browser_reload",
    "whitenoise.runserver_nostatic",
    "django_extensions",
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# These settings work for the default dev database.
# You can run this database using docker compose.
# Look inside dev_db/README.md for details!!

DB_USER = os.environ.get("DATABASE_USER", "pguser")  # noqa: F405
DB_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1")  # noqa: F405
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")  # noqa: F405
DB_NAME = os.environ.get("DATABASE_NAME", "db")  # noqa: F405
DB_PORT = os.environ.get("DATABASE_PORT", 5432)  # noqa: F405

DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
}

# Email Sending settings
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "rakoto.olive42@gmail.com")
DEFAULT_FROM_NAME = "DjangoCon Africa 2025"

# For development (console output)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# For production (Mailjet)
# Mailjet configuration
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# MAILJET_API_KEY = config('MAILJET_API_KEY')
# MAILJET_API_SECRET = config('MAILJET_SECRET_KEY')

EMAIL_FILE_PATH = BASE_DIR / "gitignore/emails"  # noqa: F405
FEATURE_FLAGS = {"USER_LOGIN_REG": False}
# noqa: F405
WAGTAIL_SITE_NAME = "DjangoCon Africa"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# Basic development logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': 'INFO',  # Only show INFO and above
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Suppress Django DEBUG logs
            'propagate': False,
        },
        'autoreload': {
            'handlers': ['console'],
            'level': 'WARNING',  # Suppress autoreload DEBUG logs
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'WARNING',  # Suppress Wagtail DEBUG logs
            'propagate': False,
        },
    },
}