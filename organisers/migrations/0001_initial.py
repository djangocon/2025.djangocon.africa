from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organiser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        help_text="Full name of the organiser",
                        unique=True,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        max_length=255, help_text="Role or responsibility"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="Photo of the organiser",
                        null=True,
                        upload_to="organisers/",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        blank=True, help_text="Country", max_length=2
                    ),
                ),
                (
                    "social_links",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Social links as a JSON object",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(default=1, help_text="Display order"),
                ),
                (
                    "approved",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this organiser is approved for display",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "name", "id"],
                "verbose_name": "Organiser",
                "verbose_name_plural": "Organisers",
            },
        ),
    ]
