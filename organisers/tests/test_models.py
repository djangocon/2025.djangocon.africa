import pytest
from organisers.models import Organiser


class TestOrganiser:
    @pytest.mark.django_db
    def test_organiser_creation(self):
        organiser = Organiser.objects.create(
            name="Jane Doe",
            role="Digital content",
            country="TZ",
            social_links={
                "github": "https://github.com/janedoe",
                "twitter": "https://twitter.com/janedoe",
            },
            order=1,
        )
        assert organiser.name == "Jane Doe"
        assert organiser.role == "Digital content"
        assert organiser.country.code == "TZ"
        assert organiser.social_links["github"] == "https://github.com/janedoe"
        assert organiser.order == 1
        assert organiser.approved is False  # Default value

    @pytest.mark.django_db
    def test_organiser_approved_field(self):
        """Test the approved field functionality"""
        organiser = Organiser.objects.create(
            name="Test Organiser", role="Test Role", approved=True, order=1
        )
        assert organiser.approved is True

    @pytest.mark.django_db
    def test_organiser_ordering(self):
        Organiser.objects.create(name="A", role="", order=2)
        Organiser.objects.create(name="B", role="", order=1)
        organisers = Organiser.objects.all()
        assert organisers[0].name == "B"
        assert organisers[1].name == "A"

    @pytest.mark.django_db
    def test_organiser_str(self):
        organiser = Organiser.objects.create(name="Jane Doe", role="", order=1)
        assert str(organiser) == "Jane Doe"
