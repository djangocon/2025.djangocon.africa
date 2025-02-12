from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class OpportunityGrants(models.Model):
    link = models.URLField(
        max_length=512,
        help_text=_('Link to Opportunity Grant'),
        blank=True,
    )

    is_open = models.BooleanField(
        default=False,
        help_text=_("Whether the button is an open state."),
    )

    closing_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("The date and time when the button should be considered closed."),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time when the Opportunity Grant was created.")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time when the Opportunity Grant was updated.")
    )

    def save(self, *args, **kwargs):
        if not self.pk and OpportunityGrants.objects.exists():
            raise ValidationError("Only one Opportunity Grant can be saved.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Opportunity Grant"



