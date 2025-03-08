from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_home, name="page_home"),
    path("coc", views.page_coc, name="page_coc"),
    path("speaking", views.page_speaking, name="page_speaking"),
    path("static-news/<slug:slug>/", views.page_news_detail, name="page_news_detail"),
    path("speaking", views.page_speaking, name="speaking"),
    path("speaker_resources", views.page_speaker_resources, name="speaker_resources"),
    path("sponsor_us", views.page_sponsor_us, name="sponsor_us"),
    path("opportunity_grants", views.opportunity_grants, name="opportunity_grants"),
]
