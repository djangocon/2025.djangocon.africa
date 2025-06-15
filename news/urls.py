from django.urls import path, include, re_path
from django.conf import settings

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path(settings.CMS_PATH, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
]
