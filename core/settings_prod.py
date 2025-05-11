from .settings_base import *  # noqa: F403
from decouple import config
import dj_database_url
import os

ALLOWED_HOSTS = ["2025.djangocon.africa"]
BASE_URL = "https://2025.djangocon.africa"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET"]  # noqa: F405

DEBUG = False


DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa: F405
    )
}


# email config - to be setted in another feature
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
MAILJET_API_KEY = config('MAILJET_API_KEY')
MAILJET_API_SECRET = config('MAILJET_SECRET_KEY')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default="hello@djangocon.africa")
DEFAULT_FROM_NAME = 'DjangoCon Africa 2025'

# Production-specific logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB per file
            'backupCount': 5,  # Keep 5 backup files
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
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}