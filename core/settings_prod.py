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
