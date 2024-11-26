from django import forms
from . import models


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
