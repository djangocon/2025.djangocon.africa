from .settings_base import *  # noqa: F403
import dj_database_url

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "2025.djangocon.africa"]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET"]  # noqa: F405

DEBUG = False


DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa: F405
    )
}
