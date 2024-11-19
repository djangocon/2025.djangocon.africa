from .settings_base import *
import os
import dj_database_url

SECRET_KEY = "not really a secret"
DEBUG = True

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INSTALLED_APPS += [
    "django_browser_reload",
    "whitenoise.runserver_nostatic",
    "django_extensions",
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# These settings work for the default dev database.
# You can run this database using docker compose.
# Look inside dev_db/README.md for details!!

DB_USER =  os.environ.get("DATABASE_USER", "pg_user")
DB_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")
DB_NAME = os.environ.get("DATABASE_NAME","db")
DB_PORT = os.environ.get("DATABASE_PORT", 6543)

DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'
