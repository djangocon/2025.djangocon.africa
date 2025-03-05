from django.urls import path, include, re_path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("cms/", include(wagtailadmin_urls)), # TODO: make the admin fetch from the env
    path("documents/", include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
]

