from .settings_base import *

import os


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "2025.djangocon.africa"]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET"]

DEBUG = False
