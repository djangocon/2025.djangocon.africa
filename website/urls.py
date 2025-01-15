from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_home, name="page_home"),
    path("coc", views.page_coc, name="page_coc"),
]
