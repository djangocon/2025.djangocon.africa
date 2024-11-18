from .settings_base import *


SECRET_KEY = "not really a secret"
DEBUG = True

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INSTALLED_APPS += [
    "django_browser_reload",
    "whitenoise.runserver_nostatic",
]
