from django import forms
from . import models
from django.utils.translation import gettext_lazy as _


class ProposalForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = [
            "title",
            "proposal_type",
            "track",
            "description",
            "private_notes",
            "additional_speaker_emails",
            "audience_level",
            "accessibility_requests",
        ]

        help_texts = {
            "private_notes": _(
                "Notes to the reviewer. These notes will not be displayed publicly"
            ),
            "additional_speaker_emails": _(
                "Are there other speakers involved in your talk? List only their email addresses here"
            ),
        }
