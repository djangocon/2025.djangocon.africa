from django.urls import path
from .views import OrganisersListView

urlpatterns = [
    path("", OrganisersListView.as_view(), name="organisers"),
]
