from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# Create your models here.


class Organiser(models.Model):
    name = models.CharField(
        max_length=255, unique=True, help_text=_("Full name of the organiser")
    )
    role = models.CharField(max_length=255, help_text=_("Role or responsibility"))
    photo = models.ImageField(
        upload_to="organisers/",
        blank=True,
        null=True,
        help_text=_("Photo of the organiser"),
    )
    country = CountryField(blank=True, help_text=_("Country"))
    social_links = models.JSONField(
        default=dict, blank=True, help_text=_("Social links as a JSON object")
    )
    order = models.PositiveIntegerField(default=1, help_text=_("Display order"))
    approved = models.BooleanField(
        default=False, help_text=_("Whether this organiser is approved for display")
    )

    class Meta:
        ordering = ["order", "name", "id"]
        verbose_name = _("Organiser")
        verbose_name_plural = _("Organisers")

    def __str__(self):
        return self.name
