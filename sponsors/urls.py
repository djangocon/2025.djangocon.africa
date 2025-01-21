from django.urls import re_path

from sponsors.views import SponsorsDetailView

urlpatterns = [
    re_path(r"^$", SponsorsDetailView.as_view(), name="sponsors"),
]

