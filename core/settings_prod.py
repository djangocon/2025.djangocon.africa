from .settings_base import *  # noqa: F403
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


MAILJET_API_SECRET=os.environ.get("MJ_APIKEY_SECRET_PROD")
MAILJET_APIKEY_PUBLIC=os.environ.get("MJ_APIKEY_PUBLIC_PROD")
DEFAULT_FROM_EMAIL=os.environ.get("SENDER_EMAIL_PROD", "hello@djangocon.africa")


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = str(os.getenv('EMAIL_USER'))
# EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_PASSWORD'))
