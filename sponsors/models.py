from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class File(models.Model):
    """File for use in sponsor and sponsorship package description."""
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        help_text=_("A Description of the file.")
    )
    item = models.FileField(
        upload_to='sponsors_files'
    )

    def __str__(self):
        return u"%s (%s)" % (self.name, self.item.url)


class SponsorshipPackage(models.Model):
    """A description of a sponsorship package."""
    order = models.IntegerField(default=1)
    name = models.CharField(
        max_length=255,
        help_text=_("The name of the sponsorship package.")
    )
    number_available = models.IntegerField(
        null=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=20,
        default="$",
        help_text=_("Currency symbol of the sponsorship package.")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text=_("The amount of the sponsorship package.")
    )
    short_description = models.TextField(
        help_text=_("A short description of the sponsorship package.")
    )
    files = models.ManyToManyField(
        File,
        related_name="packages",
        blank=True,
        help_text=_("The files of the sponsorship package.")
    )
    symbol = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("The symbol of the sponsorship package.")
    )

    class Meta:
        ordering = ["order", "-amount", "name"]

    def __str__(self):
        return u"%s (amount: %.0f)" % (self.name, self.amount,)


class Sponsor(models.Model):
    """A conference sponsor."""
    order = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    packages = models.ManyToManyField(
        SponsorshipPackage,
        related_name="sponsors",
    )
    description = models.TextField(
        help_text=_("A description of the sponsor.")
    )
    url = models.URLField(
        default="",
        blank=True,
        help_text=_("The URL of the sponsor if needed.")
    )
    hiring = models.BooleanField(
        default=False,
        help_text=_("Whether the sponsor is hiring or not.")
    )
    hiring_url = models.URLField(
        default="",
        blank=True,
        help_text=_("Hiring URL of the sponsor.")
    )

    def __str__(self):
        return u"%s" % (self.name,)

    class Meta:
        ordering = ["order", "name", "id"]


class TaggedFile(models.Model):
    """Tags for files associated with a given sponsor"""
    tag_name = models.CharField(
        max_length=255,
        null=False,
        help_text=_("The name of the tag.")
    )
    tagged_file = models.ForeignKey(
        File,
        on_delete=models.CASCADE
    )
    sponsor = models.ForeignKey(
        Sponsor,
        related_name="files",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return u"%s - (%s)" % (self.sponsor.name, self.tag_name,)

