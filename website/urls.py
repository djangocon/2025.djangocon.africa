from django.urls import path

from . import views

app_name = "website"


urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("coc/", views.coc, name="coc"),
    path("information/", views.information, name="information"),
    path("team/", views.team, name="team"),
    path("talks/", views.talks, name="talks"),
    path("contact/", views.contact, name="contact"),
    path("grants/", views.grants, name="grants"),
    path("venue/", views.venue, name="venue"),
    path("cfp/", views.cfp, name="cfp"),
    path("schedule/", views.schedule, name="schedule"),
    path("sponsor/", views.sponsor, name="sponsor"),
    path("sponsors/", views.sponsors, name="sponsors"),
]
