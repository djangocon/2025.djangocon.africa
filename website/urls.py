from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_home, name="page_home"),
    path("coc", views.page_coc, name="page_coc"),
    path("speaking", views.page_speaking, name="page_speaking"),
    path("news/<slug:slug>/", views.page_news_detail, name="page_news_detail"),
]
