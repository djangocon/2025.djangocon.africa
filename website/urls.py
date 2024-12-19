from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_home, name="page_home"),
    path("code_of_conduct", views.page_code_of_conduct, name="page_code_of_conduct"),
]
