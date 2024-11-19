from .settings_base import *

import os
import dj_database_url

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "2025.djangocon.africa"]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET"]

DEBUG = False


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DB_USER = os.environ.get("DATABASE_USER")
DB_HOST = os.environ.get("DATABASE_HOST")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_NAME = os.environ.get("DATABASE_NAME")
DB_PORT = os.environ.get("DATABASE_PORT", 5432)

DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
}


# email config - to be setted in another feature 
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = str(os.getenv('EMAIL_USER'))
# EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_PASSWORD'))
