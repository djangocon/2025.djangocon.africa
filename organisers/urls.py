from django.urls import path
from .views import (
    OrganisersListView,
    OrganiserSubmissionView,
    OrganiserSubmissionSuccessView,
)

urlpatterns = [
    path("", OrganisersListView.as_view(), name="organisers"),
    path("submit/", OrganiserSubmissionView.as_view(), name="organiser_submission"),
    path(
        "submit/success/",
        OrganiserSubmissionSuccessView.as_view(),
        name="organiser_submission_success",
    ),
]
