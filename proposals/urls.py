from django.urls import path

from . import views

urlpatterns = [
    path("my_proposals", views.my_proposals, name="my_proposals"),
    path(
        "my_proposals/<int:proposal_id>/delete",
        views.action_delete_my_proposal,
        name="action_delete_my_proposal",
    ),
    path(
        "my_proposals/create",
        views.create_proposal,
        name="create_proposal",
    ),
    # path(
    #     "my_proposals/create",
    #     views.action_create_proposal_submit,
    #     name="action_create_proposal_submit",
    # ),
]
