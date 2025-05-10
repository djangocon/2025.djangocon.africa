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
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
DEFAULT_FROM_NAME = 'DjangoCon Africa 2025'