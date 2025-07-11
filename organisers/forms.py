from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Organiser

COMMON_INPUT_CLASSES = (
    "bg-gray-50 border border-gray-200 rounded-lg w-full px-4 py-2.5 "
    "focus:outline-none focus:ring-1 focus:ring-deepTeal focus:border-deepTeal transition"
)
COMMON_FILE_CLASSES = (
    "bg-gray-50 border border-gray-200 rounded-lg w-full px-4 py-2 "
    "focus:outline-none focus:ring-1 focus:ring-deepTeal focus:border-deepTeal transition"
)


class OrganiserSubmissionForm(forms.ModelForm):
    twitter = forms.URLField(
        label="Twitter/X",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://x.com/username",
            }
        ),
    )
    linkedin = forms.URLField(
        label="LinkedIn",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://linkedin.com/in/username",
            }
        ),
    )
    github = forms.URLField(
        label="GitHub",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://github.com/username",
            }
        ),
    )
    mastodon = forms.URLField(
        label="Mastodon",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://mastodon.social/@username",
            }
        ),
    )
    bluesky = forms.URLField(
        label="Bluesky",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://bsky.app/profile/username",
            }
        ),
    )
    web = forms.URLField(
        label="Website",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": COMMON_INPUT_CLASSES,
                "placeholder": "https://yourwebsite.com",
            }
        ),
    )

    class Meta:
        model = Organiser
        fields = ["name", "role", "photo", "country"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": COMMON_INPUT_CLASSES, "placeholder": "Your full name"}
            ),
            "role": forms.TextInput(
                attrs={
                    "class": COMMON_INPUT_CLASSES,
                    "placeholder": "Your role (e.g. Organizer)",
                }
            ),
            "photo": forms.FileInput(
                attrs={"class": COMMON_FILE_CLASSES, "accept": "image/*"}
            ),
            "country": CountrySelectWidget(attrs={"class": COMMON_INPUT_CLASSES}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].required = False
        # Prefill social fields from instance if editing
        social = (
            self.instance.social_links
            if self.instance and self.instance.social_links
            else {}
        )
        for key in ["twitter", "linkedin", "github", "mastodon", "bluesky", "web"]:
            self.fields[key].initial = social.get(key, "")

    def clean(self):
        cleaned_data = super().clean()
        # Build social_links dict from individual fields
        social_links = {}
        for key in ["twitter", "linkedin", "github", "mastodon", "bluesky", "web"]:
            val = cleaned_data.get(key)
            if val:
                social_links[key] = val
        self.cleaned_data["social_links"] = social_links

        name = cleaned_data.get("name", "").strip()
        role = cleaned_data.get("role", "").strip()
        if name and role:
            exists = Organiser.objects.filter(
                name__iexact=name, role__iexact=role
            ).exists()
            if exists:
                self.add_error(
                    "name",
                    "An organiser with this name and role has already been submitted.",
                )
                self.add_error(
                    "role",
                    "An organiser with this name and role has already been submitted.",
                )
        return cleaned_data

    def save(self, commit=True):
        self.instance.social_links = self.cleaned_data.get("social_links", {})
        return super().save(commit=commit)
